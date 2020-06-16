import requests
import datetime
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
from lxml import html
import matplotlib.pyplot as plt
import numpy as np
from requests.packages.urllib3.connectionpool import HTTPConnectionPool
from time import sleep

"""
Usefull link: https://kazuar.github.io/scraping-tutorial/
Could be usefull: https://medium.com/hackernoon/how-to-run-asynchronous-web-requests-in-parallel-with-python-3-5-without-aiohttp-264dc0f8546
https://dev.to/rhymes/how-to-make-python-code-concurrent-with-3-lines-of-code-2fpe
https://stackoverflow.com/questions/15752973/python-how-can-i-send-multiple-http-requests-at-the-same-time-like-fork
"""

# NUM_OF_REQUESTS = 200
# NUM_OF_URLS_MULTIPLE = 5
NUM_OF_REQUESTS = 1000
NUM_OF_URLS_MULTIPLE = 1

def get_it(url, session, proxies=None):
    time1 = datetime.datetime.now()
    r = session.get(url,proxies=proxies)
    time2 = datetime.datetime.now()
    return r.status_code, (time2-time1).days/86400.0 + (time2-time1).seconds + (time2-time1).microseconds/1000000, time1, time2, url


def sending_multiple_requests(url, session, proxies=None):
    urls = [url] * NUM_OF_REQUESTS
    with PoolExecutor(max_workers=NUM_OF_REQUESTS * NUM_OF_URLS_MULTIPLE) as executor:
        # res = executor.map(get_it, urls, session)
        args = ((url, session,proxies) for url in urls)
        res =executor.map(lambda p: get_it(*p), args)# (*p) does the unpacking part
        return res

def login(proxies = None):
    session_requests = requests.session()
    login_url = "https://pc6m9n5jrh.execute-api.us-east-2.amazonaws.com/dev/login/"
    result = session_requests.get(login_url, proxies=proxies)
    tree = html.fromstring(result.text)
    authenticity_token = list(set(tree.xpath("//input[@name='csrfmiddlewaretoken']/@value")))[0]
    payload = {"username": "2516670@intel.com", "password": "2516670", "csrfmiddlewaretoken": authenticity_token}
    result = session_requests.post(login_url, data=payload, headers=dict(referer=login_url))
    return session_requests


def write_multiple_requests_to_csv(url_res_generator, ax, color, label):
    response_times = []
    multiple_requests_data = ""
    for result_i in url_res_generator:
        row = ""
        for j in range(len(result_i)):
            row += str(result_i[j])+','
            if j == 1:
                response_times.append(result_i[1])
        row = row[:-1]+"\n"
        multiple_requests_data += row
        print(row)

    # f = open("multiple_requests_get_1_url.csv", "a")
    f = open("multiple_requests_get_1_url_us_proxy_2.csv", "a")
    f.write(multiple_requests_data)
    f.close()

    # t = np.arange(1., NUM_OF_REQUESTS + 1, 1)
    # # plt.plot(t, response_times[0:999], 'r-', t, response_times[1000:1999], 'bs-', t, response_times[2000:2999], 'g-',
    # #          t, response_times[3000:3999], 'c-', t, response_times[4000:4999], 'y-')
    # ax.plot(t, response_times, color, label=label)
    # ax.legend()


def determine_color_and_label(url):
    if url == 'https://pc6m9n5jrh.execute-api.us-east-2.amazonaws.com/dev/users/mycubic/':
        return 'r-', "my cubic"
    if url == 'https://pc6m9n5jrh.execute-api.us-east-2.amazonaws.com/dev/focal_point/floorstatistics':
        return 'bs-', "focal point floor statistics"
    if url == 'https://pc6m9n5jrh.execute-api.us-east-2.amazonaws.com/dev/focal_point/assignments/':
        return 'g-', "focal point assignments"
    if url == 'https://pc6m9n5jrh.execute-api.us-east-2.amazonaws.com/dev/space_planner/statistics/campuses/':
        return 'c-', "space planner statistics"
    if url == 'https://pc6m9n5jrh.execute-api.us-east-2.amazonaws.com/dev/facilities/cubics/':
        return 'y-', "all cubics"


def exp1(session):
    # get_urls = ['https://pc6m9n5jrh.execute-api.us-east-2.amazonaws.com/dev/users/mycubic/',
    #             'https://pc6m9n5jrh.execute-api.us-east-2.amazonaws.com/dev/focal_point/floorstatistics',
    #             'https://pc6m9n5jrh.execute-api.us-east-2.amazonaws.com/dev/focal_point/assignments/',
    #             'https://pc6m9n5jrh.execute-api.us-east-2.amazonaws.com/dev/space_planner/statistics/campuses/',
    #             'https://pc6m9n5jrh.execute-api.us-east-2.amazonaws.com/dev/facilities/cubics/']
    # get_urls = ['https://pc6m9n5jrh.execute-api.us-east-2.amazonaws.com/dev/facilities/cubics/',
    #             'https://pc6m9n5jrh.execute-api.us-east-2.amazonaws.com/dev/users/mycubic/',
    #             'https://pc6m9n5jrh.execute-api.us-east-2.amazonaws.com/dev/focal_point/assignments/']
    get_urls = ['https://pc6m9n5jrh.execute-api.us-east-2.amazonaws.com/dev/users/mycubic/']
    ax = plt.subplot(111)
    for url in get_urls:
        res = sending_multiple_requests(url, session)
        color, label = determine_color_and_label(url)
        write_multiple_requests_to_csv(res, ax, color, label)

def exp1_c(session):
    get_urls = ['https://pc6m9n5jrh.execute-api.us-east-2.amazonaws.com/dev/users/mycubic/']
    ax = plt.subplot(111)
    us_ip = "http://104.129.202.148:10103"
    proxies = {"http": "104.129.202.148:10103", 'https': "104.129.202.148:10103"}
    for url in get_urls:
        res = sending_multiple_requests(url, session, proxies)
        color, label = determine_color_and_label(url)
        write_multiple_requests_to_csv(res, ax, color, label)

def exp1_d(session):
    get_urls = ['https://pc6m9n5jrh.execute-api.us-east-2.amazonaws.com/dev/users/mycubic/',
                'https://pc6m9n5jrh.execute-api.us-east-2.amazonaws.com/dev/focal_point/floorstatistics',
                'https://pc6m9n5jrh.execute-api.us-east-2.amazonaws.com/dev/focal_point/assignments/',
                'https://pc6m9n5jrh.execute-api.us-east-2.amazonaws.com/dev/space_planner/statistics/campuses/',
                'https://pc6m9n5jrh.execute-api.us-east-2.amazonaws.com/dev/facilities/cubics/']
    # get_urls = ['https://pc6m9n5jrh.execute-api.us-east-2.amazonaws.com/dev/users/mycubic/']
    ax = plt.subplot(111)
    for url in get_urls:
        res = sending_multiple_requests(url, session)
        color, label = determine_color_and_label(url)
        write_multiple_requests_to_csv(res, ax, color, label)


def exp1_e(session, url):
    res = get_it(url, session)
    row = ""
    for result_i in res:
        row += str(result_i) + ','
    print(row)
    row = row[:-1] + "\n"
    f = open("one_request_504_urls_v2.csv", "a")
    f.write(row)
    f.close()


def exp2(session, country):
    i = 0
    while i < 10:
        try:
            # get_urls = ['https://pc6m9n5jrh.execute-api.us-east-2.amazonaws.com/dev/users/mycubic/',
            #             'https://pc6m9n5jrh.execute-api.us-east-2.amazonaws.com/dev/focal_point/floorstatistics',
            #             'https://pc6m9n5jrh.execute-api.us-east-2.amazonaws.com/dev/focal_point/assignments/',
            #             'https://pc6m9n5jrh.execute-api.us-east-2.amazonaws.com/dev/space_planner/statistics/campuses/',
            #             'https://pc6m9n5jrh.execute-api.us-east-2.amazonaws.com/dev/facilities/cubics/']
            # get_urls = ['https://pc6m9n5jrh.execute-api.us-east-2.amazonaws.com/dev/facilities/cubics/',
            #             'https://pc6m9n5jrh.execute-api.us-east-2.amazonaws.com/dev/users/mycubic/',
            #             'https://pc6m9n5jrh.execute-api.us-east-2.amazonaws.com/dev/focal_point/assignments/']
            get_urls = ['https://pc6m9n5jrh.execute-api.us-east-2.amazonaws.com/dev/users/mycubic/']
            proxy_orbit_url = "https://api.proxyorbit.com/v1/?token=A1MSGdShFJYc8XtKK-TpuEDqEPLw58yTcgoZA6t9ZFs&location={country}"
            # presp = requests.get(proxy_orbit_url.format(country=country))
            # ip = presp.json()['curl']
            # https_ip = ip.replace('http', 'https')
            # proxies = {"http": ip, 'https': https_ip}
            ip = "http://155.138.138.36:8080"
            proxies = {"http": "http://155.138.138.36:8080", 'https': "http://155.138.138.36:8080"}
            url = get_urls[0]

            time1 = datetime.datetime.now()
            resp = session.get(url, proxies=proxies)
            time2 = datetime.datetime.now()

            delta = time2-time1
            time_delta = delta.days/86400.0 + delta.seconds + delta.microseconds/1000000
            print(country,resp.status_code,time1,time2,time_delta,ip)
            i += 1
        except Exception as e:
            print("failed")
            pass

def exp3(session):
    get_urls = ['https://pc6m9n5jrh.execute-api.us-east-2.amazonaws.com/dev/users/mycubic/']
    times = [60*60*2, 60*60*24]
    for time in times:
        print("checking now: " + str(time))
        i = 0
        while i < 10:
            sleep(time)
            line_str = ""
            line = get_it(get_urls[0], session)
            for item in line:
                line_str += str(item)+","
            print(line_str)
            f = open("times_"+str(time)+".csv", "a")
            f.write(line_str[:-1]+"\n")
            f.close()
            i = i+1



def main():
    session = login()
    print("logged in")
    # exp1(session)
    #countries = ["CA"]
    #for country in countries:
        #exp2(session, country)
        # sleep(10)

    # plt.title('Multiple Requests To Website')
    # plt.ylabel('response time(seconds)')
    # plt.show()
    exp3(session)
    # get_urls_504 =['https://pc6m9n5jrh.execute-api.us-east-2.amazonaws.com/dev/focal_point/floorstatistics',
    #             'https://pc6m9n5jrh.execute-api.us-east-2.amazonaws.com/dev/space_planner/statistics/campuses/']
    # for url in get_urls_504:
    #     exp1_e(session, url)
    # exp1_c(session)
    return


if __name__ == "__main__":
    main()