import http.client
import urllib.parse
from lxml import html
import re
import json
import requests
import argparse
from datetime import datetime
import os, ssl
from TikTokApi import TikTokApi
import numpy as nump
import csv
#https://www.tiktok.com/@slow_mm/video/7002232802255162626
# parser = argparse.ArgumentParser()
# parser.add_argument("url")
user_list =[]
single_user_links=[]
url_dict = {"content":[],
"d":""}


def python_unique (list_3):
    n = nump.array(list_3)
    list_final = nump.unique (n)
    return list_final.tolist()

def read_csv_into_list():
    global single_user_links
    with open('input/input.csv', 'r') as f:
        # no need for `list` here
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            single_user_links.append(row)

        print('list length 1=' ,len(single_user_links))
        single_user_links= python_unique(single_user_links)
        print('list length =' ,type(single_user_links))

def getUserLinks(user_name):
    url_dict.update({"content": single_user_links})
    now = datetime.now() # current date and time
    # 2021-08-31T09:00:19.241Z
    date_time_str = now.strftime("%Y-%m-%dT%H:%M:%S")
    url_dict.update({"d":date_time_str })

def getCookie():
    conn = http.client.HTTPSConnection("dltik.com")
    payload = ''
    conn.request("GET", "/?hl=vi", payload)
    res = conn.getresponse()
    if res.status == 200:
        cookie = res.headers['Set-Cookie']
        html = res.read().decode("utf-8")
        token = ''
        match = re.search(r"<input name=\"__RequestVerificationToken\"[^>]*value=\"([^ ]+)\"", html, re.MULTILINE)
        if match:
            token = match.group(1)
        return [cookie, token]
    return ''

def getDownloadUrl(url, cookie,i):
    try:
        print('url = ',url)
        conn = http.client.HTTPSConnection("dltik.com")
        cookies = cookie[0].split(';')[0].split('=')
        payload = 'm=getlink&url=' + urllib.parse.quote(url, safe='') + '&__RequestVerificationToken=' + urllib.parse.quote(cookie[1], safe='')
        headers = {
            'Cookie': cookies[0] + '=' + cookies[1] + ';',
            'content-type': 'application/x-www-form-urlencoded'
        }
        conn.request("POST", "/?hl=vi", payload, headers)
        res = conn.getresponse()
        if res is not None:
            data = res.read()
            # print(json.dumps(json.loads(data.decode("utf-8")), indent=4, sort_keys=True))
            datajs =json.loads(data.decode("utf-8"))
            # print(datajs)
            # urls='https://v39-as.tiktokcdn.com/211e0df35b3b82b259aa785fa68fcc3b/612a0f83/video/tos/useast2a/tos-useast2a-pve-0037-aiso/af8bdb1c3d3c4df0b64dc6ba35285337/?a=1233&br=1602&bt=801&cd=0%7C0%7C0&ch=0&cr=0&cs=0&cv=1&dr=0&ds=6&er=&ft=98ZmAekh4kag3&l=20210828042700010245173118548D78DE&lr=all&mime_type=video_mp4&net=0&pl=0&qs=0&rc=M3U2NWU6ZmhrNzMzZjgzM0ApZmQ7aTQ2NTw0N2Q4PDU7aGctLWRxcjRvLWdgLS1kL2NzczNgXjFjNWBhYjYuNV8tMDA6Yw%3D%3D&vl=&vr='
            # r = requests.get(str(datajs["data"]["destinationUrl"]))
            r = requests.get(datajs["data"]["destinationUrl"])
            name = str(datajs["data"]["desc"])
            cleanString = re.sub('\W+', '', name)
            print(cleanString)
            with open('download/'+str(i) + cleanString +  '.mp4' , 'wb') as fd:
                fd.write(r.content)
    except Exception as ex:
        print(ex)
        pass
if __name__ == '__main__':
    # args = parser.parse_args()
    i = 0
    if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
        ssl._create_default_https_context = ssl._create_unverified_context
    read_csv_into_list()
    getUserLinks("")
    cookie = getCookie()
    
    for url_dict in url_dict["content"]:
        getDownloadUrl(url_dict, cookie,i)
        i=i+1

