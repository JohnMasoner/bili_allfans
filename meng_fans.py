# coding=utf-8
import requests
from bs4 import BeautifulSoup
import json
import csv
import chardet
import time
import pandas as pd
import tqdm

cookie = ''

header = {
    'cookie':cookie,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
}


def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)


def get_data(url):
    response = requests.get(url,headers = header)
    
    json_data = json.loads(response.text)
    if json_data['code'] == 22007:
        print('请更换cookie，或非up本人仅可查看5页')
        exit()
    # 获取粉丝总数，为之后计算页数

    page_fans_list = json_data['data']['list']
    return page_fans_list

def write_csv(mid,name,mtime):
    res = pd.DataFrame()

    res['mid'] = mid # 用戶編號
    res['name'] = name # 名字
    res['mtime'] = mtime # 關注時間

    res.to_csv('FollowerData.csv', index = None)


if __name__ == '__main__':
    AllFansNum = 27221
    # 此处第一个加一为抵消向下取证带来的数值变化 ， 第二个加一为循环时并不会循环到本位
    AllPageNum = 27221//20 + 1 + 1
    vmid = int(input('输入你要爬去的userid：'))
    mid = []
    name = []
    mtime = []

    for pn in range(1,AllPageNum):
        url = f'https://api.bilibili.com/x/relation/followers?vmid={vmid}&pn={pn}&ps=20'
        fans_data = get_data(url)
        for i in fans_data:
            mid.append(i['mid'])
            name.append(i['uname'])
            bj_mtime = TimeStampToTime(i['mtime'])
            mtime.append(bj_mtime)
            time.sleep(0.5)
        print(f'{pn}/{AllPageNum}已完成写入')
        time.sleep(0.5)
        
        write_csv(mid, name, mtime)


