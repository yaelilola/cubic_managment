import pandas as pd
import sqlite3
from sqlite3 import IntegrityError
from django.contrib.auth.hashers import make_password
from sqlalchemy import create_engine
import psycopg2
import sys
import os

POSTGRES_ADDRESS = os.environ['DB_HOST']
POSTGRES_PORT = os.environ['DB_PORT']
POSTGRES_USERNAME = os.environ['DB_USER']
POSTGRES_PASSWORD = os.environ['DB_PASSWORD']
POSTGRES_DBNAME = os.environ['DB_NAME']


# find the n'th delimeter (the needle, which is '-') in the cubic barcode
def findnth(haystack, needle, n):
    parts = haystack.split(needle, n+1)
    if len(parts) <= n+1:
        return -1
    return len(haystack)-len(parts[-1])-len(needle)


# get all campuses for the Campus model(their id's) from the space_details_sheet
def get_campuses(space_details_sheet):
    return space_details_sheet['City'].drop_duplicates().to_frame().rename(columns={"City": "id"})


# get all buildings for the Building model (their id's and campuses) from the space_details_sheet
def get_buildings(space_details_sheet):
    return (space_details_sheet[['City', 'Building ID']]).drop_duplicates().rename(columns={"City": "campus_id",
                                                                                            "Building ID": "id"})


# get all floors for the Floor model (their id's, campus , building, num) from the space_details_sheet
def get_floors(space_details_sheet):
    df = (space_details_sheet[['Building ID', 'Floor Name']]).drop_duplicates().\
        rename(columns={"Floor Name": "floor_num", "Building ID": "building_id"})
    df['id'] = df['building_id'] + "-" + df['floor_num']
    return df


# get all spaces for the Space model (their id's, campus , building, floor id, area ) from the space_details_sheet
def get_spaces(space_details_sheet):
    space_details_sheet = add_space_id(space_details_sheet)
    df = space_details_sheet[space_details_sheet['Current Use Space Class']
        .isin(['Cube', '120', 'AWS', 'Bench', 'Low Density Lab', 'High Density Lab'])]
    df = (df[['City', 'Building ID', 'Space_ID', 'Area (SF)', 'Floor Name']]).drop_duplicates()
    df['floor_id'] = df['Building ID'] + "-" + df['Floor Name']
    df = df.groupby(['City', 'Building ID', 'Space_ID', 'floor_id'], as_index=False).sum()
    df = df.rename(columns={'City': 'campus_id', 'Building ID': 'building_id', 'Space_ID': 'id',
                       'Area (SF)': 'area'})
    return df


# creates the space id from the barcode and adds this column to space_details_sheet
def add_space_id(space_details_sheet):
    space_ids = []
    for bar in space_details_sheet['Bar Code'].tolist():
        space_ids.append(bar[0:(findnth(bar, "-", 2))])
    space_details_sheet['Space_ID'] = space_ids
    return space_details_sheet


"""
Parsing the xslx files in order to get the data for the cubic model.
We need both the space_detail_sheet and the personnel_directory sheet so we could get the business group that the cubic 
is assigned to. 
"""
def get_cubics(space_details_sheet, personnel_directory_sheet):
    print('get cubics')
    personnel_directory_sheet['id'] = personnel_directory_sheet['Building ID'] + "-" + \
                                            personnel_directory_sheet['Floor'] + "-" + \
                                      personnel_directory_sheet['Space Label']
    ps_df = personnel_directory_sheet[['Group', 'id']].dropna()
    ps_df = ps_df.drop_duplicates(subset='id')
    ps_df = ps_df.rename(columns={"Group": "business_group_id"})
    space_details_sheet = add_space_id(space_details_sheet)
    df = space_details_sheet[space_details_sheet['Current Use Space Class'].isin(['Cube', '120', 'AWS', 'Bench'])]
    df['type'] = df['Capacity']
    df.loc[df['type'] > 1, 'type'] = 'shared'
    df.loc[df['type'] == 1, 'type'] = 'private'
    df['floor_id'] = df['Building ID'] + "-" + df['Floor Name']
    df['id'] = df['floor_id'] + "-" + df['Space Label']
    df = df[['City', 'Building ID', 'floor_id', 'Space_ID', 'id', 'Capacity', 'Area (SF)', 'type']]\
        .rename(columns={'City': 'campus_id', 'Building ID': 'building_id', 'Space_ID': 'space_id',
                         'Area (SF)': 'area', 'Capacity': 'capacity'})
    df['name'] = 'Cubic'
    joined = df.join(ps_df.set_index('id'), on='id')
    joined = joined.drop_duplicates(subset='id').dropna(subset=['id'])
    print('finish get cubics')
    return joined


# gets all labs (for the Lab model) from the space_details_sheet (get their id, floor_id, building id, space id,
# type, area)
def get_labs(space_details_sheet):
    print('get labs')
    space_details_sheet = add_space_id(space_details_sheet)
    df = space_details_sheet[space_details_sheet['Current Use Space Class']
        .isin(['Low Density Lab', 'High Density Lab'])]
    df['floor_id'] = df['Building ID'] + "-" + df['Floor Name']
    df['id'] = df['floor_id'] + df['Space Label']
    df = df[['City', 'Building ID', 'floor_id', 'Space_ID', 'id', 'Current Use Space Class', 'Area (SF)']]\
        .rename(columns={'City': 'campus_id', 'Building ID': 'building_id', 'Space_ID': 'space_id',
                         'Area (SF)': 'area', 'Current Use Space Class': 'type'}).drop_duplicates(subset='id')\
        .dropna(subset=['id'])
    df['name'] = 'Lab'
    print('finish get labs')
    return df


# write the parsed data from df to table name with conn
def write_to_sqlite(table_name, df, conn):
    try:
        df.to_sql(table_name, conn, if_exists='append', index=False, chunksize=1)
    except IntegrityError as e:
        print("exception")
        print(e)
        pass


# parses all campuses from space_details_sheet to the db
def parse_campuses(space_details_sheet, conn):
    print('parse campuses')
    df = get_campuses(space_details_sheet)
    write_to_sqlite('facilities_campus', df, conn)
    print('parse after campuses')


# parses all buildings from space_details_sheet to the db
def parse_building(space_details_sheet, conn):
    print('parse building')
    df = get_buildings(space_details_sheet)
    write_to_sqlite('facilities_building', df, conn)
    print('parse after building')


# parses all floors from space_details_sheet to the db
def parse_floor(space_details_sheet, conn):
    print('parse floor')
    df = get_floors(space_details_sheet)
    write_to_sqlite('facilities_floor', df, conn)
    print('parse after floor')


# parses all spaces from space_details_sheet to the db
def parse_space(space_details_sheet, conn):
    print('parse space')
    df = get_spaces(space_details_sheet)
    write_to_sqlite('facilities_space', df, conn)
    print('after space')


# parses all cubics from space_details_sheet (using personnel_directory_sheet to get the assignments) to the db
def parse_cubic(space_details_sheet, personnel_directory_sheet, conn):
    print('parse cubic')
    df = get_cubics(space_details_sheet, personnel_directory_sheet)
    write_to_sqlite('facilities_cubic', df, conn)
    print('after parse cubic')


# parses all labs from space_details_sheet to the db
def parse_lab(space_details_sheet, conn):
    print('labs')
    df = get_labs(space_details_sheet)
    write_to_sqlite('facilities_lab', df, conn)
    print('after labs')


# parses all facilities from space_details_sheet (using personnel_directory_sheet to get the business group the cubics
# belongs to) to the db
def parse_facilities(space_details_sheet, personnel_directory_sheet, conn):
    print('parse facilities')
    parse_campuses(space_details_sheet, conn)
    parse_building(space_details_sheet, conn)
    parse_floor(space_details_sheet, conn)
    parse_space(space_details_sheet, conn)
    parse_cubic(space_details_sheet, personnel_directory_sheet, conn)
    parse_lab(space_details_sheet, conn)
    print('after parse facilities')


# parse user details (encrypted), for the CustomUser model, from personnel_directory_sheet and write it to the db
def parse_users(personnel_directory_sheet,conn):
    print('parse users')
    # personnel_directory_sheet['full_name'] = personnel_directory_sheet['First Name'] + " " + \
    #                                          personnel_directory_sheet['Last Name']
    #The line above is the real full name. The line below is the encrypted data for RDS.
    personnel_directory_sheet['full_name'] = personnel_directory_sheet['employee_number']
    pds = personnel_directory_sheet.rename(columns={'Badge Type': 'BadgeType'})
    pds = pds.query('BadgeType == "EMP"')
    # df = df.rename(columns={'WWID': 'employee_number', 'Employee Type': 'percentage', 'Active Start Date': 'start_date',
    #                  'Group': 'business_group_id', 'Email Address': 'email'})
    # df.email.fillna("NA_" + df.employee_number.astype(str) + "@intel.com", inplace=True)
    # The line above is the real full name. The line below is the encrypted data for RDS.
    df = pds.rename(columns={'Employee Type': 'percentage', 'Active Start Date': 'start_date',
                            'Group': 'business_group_id'})
    # df = pds[['WWID', 'full_name', 'Employee Type', 'Active Start Date', 'Group', 'Email Address']].fillna(value={'Employee Type': 'R'})
    # The line above is the real full name. The line below is the encrypted data for RDS.
    df = df[['employee_number', 'full_name', 'percentage', 'start_date', 'business_group_id', 'email']].fillna(value={'Employee Type': 'R'})
    passwords = []
    for emp_num in df['employee_number'].tolist():
        hashed = make_password(str(emp_num))
        passwords.append(hashed)
        print(emp_num)
        print(hashed)
    df['password'] = passwords

    df.dropna(subset=['business_group_id'])
    df = df.replace({'percentage': r'^R$'}, {'percentage': 'full_time'}, regex=True)\
        .replace({'percentage': r'^S$'}, {'percentage': 'part_time'}, regex=True)\
        .replace({'percentage': r'^I$'}, {'percentage': 'part_time'}, regex=True)
    df['active'] = True
    df['admin'] = False
    df['staff'] = False
    df['focal_point'] = False
    df['space_planner'] = False
    df['start_date'] = df['start_date'].dt.date
    write_to_sqlite('custom_user_customuser', df, conn)
    print('end parse users')


# parse all the business groups for BusinessGroup model, from the personnel_directory_sheet and writing it to the db.
def parse_business_groups(personnel_directory_sheet, conn):
    print('parse business groups')
    personnel_directory_sheet.Group.fillna("Other", inplace=True)
    df = personnel_directory_sheet[['Group']].drop_duplicates().rename(columns={'Group': 'id'})
    df['admin_group'] = False
    write_to_sqlite('custom_user_businessgroup', df, conn)
    print('after parse bg')


# parse all the assignments for AssignUserCubic model, from the personnel_directory_sheet and writing it to the db.
def parse_assign_user_cubic(personnel_directory_sheet, space_details_sheet, conn):
    print('in assign user cubic')
    spdf = space_details_sheet[space_details_sheet['Current Use Space Class'].isin(['Cube', '120', 'AWS', 'Bench'])]
    spdf['floor_id'] = spdf['Building ID'] + "-" + spdf['Floor Name']
    spdf['cubic_id'] = spdf['floor_id'] + "-" + spdf['Space Label']
    df = personnel_directory_sheet.rename(columns={'Full Cubic': 'cubic_id', 'Badge Type': 'BadgeType'})
    df = df.query('BadgeType == "EMP"')
    df = df[df.cubic_id != '--']
    df['assigned_user_id'] = df['employee_number']
    df = df[['cubic_id', 'assigned_user_id']].dropna()
    df = spdf.join(df.set_index('cubic_id'), on='cubic_id')[['assigned_user_id', 'cubic_id']].\
        dropna(subset=['assigned_user_id'])
    df = df.drop_duplicates()
    write_to_sqlite('assign_assignusercubic', df, conn)
    print('finish assign user cubic')


# parse all the new positions for NewPosition model, from the israel_positions and writing it to the db.
# currently the given database has some issues.
def parse_new_positions(israel_positions, conn):
    print('in new positions')
    israel_positions = israel_positions[
        ['Org Level 4', 'College Graduate', 'Experienced', 'Intel Contract Employee', 'Student / Intern',
         'Technical Graduate', 'College Graduate.1', 'Experienced.1', 'Intel Contract Employee.1', 'Student / Intern.1',
         'Technical Graduate.1']]
    israel_positions = israel_positions.rename(columns={'Org Level 4': 'business_group_id',
                                                        'College Graduate': 'college_graduate_internal_and_external',
                                                        'College Graduate.1': 'college_graduate_internal_only',
                                                        'Experienced': 'experienced_internal_and_external',
                                                        'Experienced.1': 'experienced_internal_only',
                                                        'Intel Contract Employee': 'intel_contract_employee_internal_and_external',
                                                        'Intel Contract Employee.1': 'intel_contract_employee_internal_only',
                                                        'Student / Intern': 'student_intern_internal_and_external',
                                                        'Student / Intern.1': 'student_intern_internal_only',
                                                        'Technical Graduate': 'technical_graduate_internal_and_external',
                                                        'Technical Graduate.1': 'technical_graduate_internal_only'})
    df = israel_positions.groupby(['business_group_id'], as_index=False).sum()
    write_to_sqlite('recruit_newposition', df, conn)
    print('after parse new positions')


# parsing the given database to postgres.
def parse2():
    loc = os.environ['LOC_PLANNING']
    loc2 = os.environ['LOC_OPEN_POSITIONS']
    xl = pd.ExcelFile(loc)
    xl2 = pd.ExcelFile(loc2)
    space_details_sheet = xl.parse('Space Details (Raw)')
    personnel_directory_sheet = xl.parse('Personnel Directory (Raw)')
    # We didn't want to upload the real employee number to the db. So, we "encrypted" it.
    personnel_directory_sheet['employee_number'] = (personnel_directory_sheet['WWID'] * 7).mod(15485863).astype(str)
    personnel_directory_sheet['email'] = personnel_directory_sheet['employee_number'].astype(str) + "@intel.com"
    israel_positions = xl2.parse('GER and GAM Open Positions').query('Country == "Israel"')
    postgres_str = ('postgresql://{username}:{password}@{ipaddress}:{port}/{dbname}').format(username=POSTGRES_USERNAME, password=POSTGRES_PASSWORD,ipaddress=POSTGRES_ADDRESS, port=POSTGRES_PORT, dbname=POSTGRES_DBNAME)
    conn = create_engine(postgres_str)
    parse_business_groups(personnel_directory_sheet, conn)
    #conn = sqlite3.connect(db_file)
    parse_facilities(space_details_sheet, personnel_directory_sheet, conn)
    parse_users(personnel_directory_sheet, conn)
    parse_assign_user_cubic(personnel_directory_sheet,space_details_sheet, conn)
    #parse_new_positions(israel_positions, conn)
    conn.dispose()


def main():
    parse2()


if __name__ == "__main__":
    main()


