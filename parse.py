import pandas as pd
import sqlite3
from sqlite3 import IntegrityError
from django.contrib.auth.hashers import make_password

def findnth(haystack, needle, n):
    parts= haystack.split(needle, n+1)
    if len(parts)<=n+1:
        return -1
    return len(haystack)-len(parts[-1])-len(needle)


def get_campuses(space_details_sheet):
    return space_details_sheet['City'].drop_duplicates().to_frame().rename(columns={"City": "id"})

def get_buildings(space_details_sheet):
    return (space_details_sheet[['City', 'Building ID']]).drop_duplicates().rename(columns={"City": "campus_id",
                                                                                            "Building ID": "id"})

def get_floors(space_details_sheet):
    df = (space_details_sheet[['Building ID', 'Floor Name']]).drop_duplicates().\
        rename(columns={"Floor Name": "floor_num", "Building ID": "building_id"})
    df['id'] = df['building_id'] + "-" + df['floor_num']
    return df

def get_spaces(space_details_sheet):
    space_details_sheet = add_space_id(space_details_sheet)
    df = space_details_sheet[space_details_sheet['Current Use Space Class']
        .isin(['Cube', 'Low Density Lab', 'High Density Lab'])]
    df = (df[['City', 'Building ID', 'Space_ID', 'Area (SF)', 'Floor Name']]).drop_duplicates()
    df['floor_id'] = df['Building ID'] + "-" + df['Floor Name']
    df = df.groupby(['City', 'Building ID', 'Space_ID', 'floor_id'], as_index=False).sum()
    df = df.rename(columns={'City': 'campus_id', 'Building ID': 'building_id', 'Space_ID': 'id',
                       'Area (SF)': 'area'})
    return df


def add_space_id(space_details_sheet):
    space_ids = []
    for bar in space_details_sheet['Bar Code'].tolist():
        space_ids.append(bar[0:(findnth(bar, "-", 2))])
    space_details_sheet['Space_ID'] = space_ids
    return space_details_sheet


def get_cubics(space_details_sheet, personnel_directory_sheet):
    personnel_directory_sheet['id'] = personnel_directory_sheet['Building ID'] + "-" + \
                                            personnel_directory_sheet['Floor'] + "-" + personnel_directory_sheet[
                                                'Space']
    ps_df = personnel_directory_sheet[['Group', 'id']].dropna()
    ps_df = ps_df.drop_duplicates(subset='id')
    space_details_sheet = add_space_id(space_details_sheet)
    df = space_details_sheet[space_details_sheet['Current Use Space Class'].isin(['Cube'])]
    df.loc[df['Capacity'] > 1, 'Capacity'] = 'shared'
    df.loc[df['Capacity'] == 1, 'Capacity'] = 'private'
    df['floor_id'] = df['Building ID'] + "-" + df['Floor Name']
    df = df[['City', 'Building ID', 'floor_id', 'Space_ID', 'Bar Code', 'Capacity', 'Area (SF)']]\
        .rename(columns={'City': 'campus_id', 'Building ID': 'building_id', 'Space_ID': 'space_id',
                         'Area (SF)': 'area', 'Bar Code': 'id', 'Capacity': 'type'})
    df['name'] = 'Cubic'
    joined = df.join(ps_df.set_index('id'), on='id')
    joined = joined[['campus_id', 'name', 'building_id', 'floor_id', 'space_id', 'id', 'type', 'area', 'Group']].\
        rename(columns={'Group': 'business_group_id'})
    # joined = joined.reset_index(drop=True)
    print(joined)
    return joined

def get_labs(space_details_sheet):
    space_details_sheet = add_space_id(space_details_sheet)
    df = space_details_sheet[space_details_sheet['Current Use Space Class']
        .isin(['Low Density Lab', 'High Density Lab'])]
    df['floor_id'] = df['Building ID'] + "-" + df['Floor Name']
    df = df[['City', 'Building ID', 'floor_id', 'Space_ID', 'Bar Code', 'Current Use Space Class', 'Area (SF)']]\
        .rename(columns={'City': 'campus_id', 'Building ID': 'building_id', 'Space_ID': 'space_id',
                         'Area (SF)': 'area', 'Bar Code': 'id',
                         'Current Use Space Class': 'type'})
    df['name'] = 'Lab'
    return df


def write_to_sqlite(table_name, df, conn):
    try:
        df.to_sql(table_name, conn, if_exists='append', index=False, chunksize=1)
    except IntegrityError as e:
        print("exception")
        print(e)
        pass


def parse_campuses(space_details_sheet, conn):
    df = get_campuses(space_details_sheet)
    write_to_sqlite('facilities_campus', df, conn)

def parse_building(space_details_sheet, conn):
    df = get_buildings(space_details_sheet)
    write_to_sqlite('facilities_building', df, conn)

def parse_floor(space_details_sheet, conn):
    df = get_floors(space_details_sheet)
    write_to_sqlite('facilities_floor', df, conn)

def parse_space(space_details_sheet, conn):
    df = get_spaces(space_details_sheet)
    write_to_sqlite('facilities_space', df, conn)

def parse_cubic(space_details_sheet, personnel_directory_sheet, conn):
    df = get_cubics(space_details_sheet, personnel_directory_sheet)
    write_to_sqlite('facilities_cubic', df, conn)

def parse_lab(space_details_sheet, conn):
    df = get_labs(space_details_sheet)
    write_to_sqlite('facilities_lab', df, conn)

def parse_facilities(space_details_sheet, personnel_directory_sheet, conn):
    parse_campuses(space_details_sheet, conn)
    parse_building(space_details_sheet, conn)
    parse_floor(space_details_sheet, conn)
    parse_space(space_details_sheet, conn)
    parse_cubic(space_details_sheet, personnel_directory_sheet, conn)
    parse_lab(space_details_sheet, conn)

def parse_users(personnel_directory_sheet,conn):
    personnel_directory_sheet['full_name'] = personnel_directory_sheet['First Name'] + " " + \
                                             personnel_directory_sheet['Last Name']
    df = personnel_directory_sheet[
        ['WWID', 'full_name', 'Employee Type', 'Active Start Date', 'Group', 'Email Address']]\
        .fillna(value={'Employee Type': 'R'})
   # df = df.head(100)
    passwords = []
    for emp_num in df['WWID'].tolist():
        #hashed = pbkdf2_sha256.using(rounds=180000, salt_size=12).hash(str(emp_num))
        hashed = make_password(str(emp_num))
        passwords.append(hashed)
        print(emp_num)
        print(hashed)
    df['password'] = passwords
    df = df.rename(columns={'WWID': 'employee_number', 'Employee Type': 'percentage', 'Active Start Date': 'start_date',
                     'Group': 'business_group_id', 'Email Address': 'email'})
    df.email.fillna("NA_" + df.employee_number.astype(str) + "@intel.com", inplace=True)
    df.business_group_id.fillna("Other", inplace=True)
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

def parse_business_groups(personnel_directory_sheet, conn):
    personnel_directory_sheet.Group.fillna("Other", inplace=True)
    df = personnel_directory_sheet[['Group']].drop_duplicates().rename(columns={'Group': 'id'})
    df['admin_group'] = False
    write_to_sqlite('custom_user_businessgroup', df, conn)

def parse_assign_user_cubic(personnel_directory_sheet, conn):
    personnel_directory_sheet['cubic_id'] = personnel_directory_sheet['Building ID'] + "-" + \
                                         personnel_directory_sheet['Floor'] + "-" + personnel_directory_sheet['Space']
    df = personnel_directory_sheet.rename(columns={'Email Address': 'email'})
    # df.email.fillna("NA_" + df.WWID.astype(str) + "@intel.com", inplace=True)
    # df['assigned_user_id'] = df['First Name'] + " " + df['Last Name'] + " " + df['email']
    df['assigned_user_id'] = df['WWID']
    df = df[['cubic_id', 'assigned_user_id']].dropna()
    write_to_sqlite('assign_assignusercubic', df, conn)

def parse_new_positions(fdo_sheet, conn):
    df = fdo_sheet.replace({'EE Type': r'^R$'}, {'EE Type': 'full_time'}, regex=True)\
        .replace({'EE Type': r'^S$'}, {'EE Type': 'part_time'}, regex=True)
    df = df[['Job Type', 'EE Type', 'Start Date', 'Group']].\
        rename(columns={'Job Type': 'name', 'EE Type': 'percentage', 'Group': 'business_group_id',
                        'Start Date': 'creation_date'})
    df['creation_date'] = df['creation_date'].dt.date
    write_to_sqlite('recruit_newposition', df, conn)

def parse2():
    loc = (r"C:\Users\owner\Desktop\uni\Sem8\industrial\parse_xlsx\ISR Planning V2.2.xlsx")
    db_file = r"C:\Users\owner\Desktop\uni\Sem8\industrial\parse_xlsx\db.sqlite3"
    xl = pd.ExcelFile(loc)
    space_details_sheet = xl.parse('Space Details (Raw)')
    personnel_directory_sheet = xl.parse('Personnel Directory (Raw)')
    conn = sqlite3.connect(db_file)
    parse_facilities(space_details_sheet, personnel_directory_sheet, conn)
    parse_users(personnel_directory_sheet, conn)
    parse_business_groups(personnel_directory_sheet, conn)
    parse_assign_user_cubic(personnel_directory_sheet, conn)
    fdo_sheet = xl.parse('FDO')
    parse_new_positions(fdo_sheet, conn)
    conn.close()









def main():
    parse2()

if __name__ == "__main__":
    main()


