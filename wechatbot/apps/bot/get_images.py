from genericpath import isdir
import re
import requests
import urllib.request
import random
from requests.models import Response
from bs4 import BeautifulSoup
import os
import time
from pyquery import PyQuery as pq, text
import io
import sys
import chardet
import gzip
import threading
import time

##################################################爬美女图片##################################################
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "sec-ch-ua": "\"Chromium\";v=\"92\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"92\"",
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "cookie": "Hm_lvt_c08bad6ac66a035b30e72722f365229b=1630671219; Hm_lpvt_c08bad6ac66a035b30e72722f365229b=1630677972"
}
##图片爬取下载绝对路径
#abspath = "F:\\alidrive2\\files"
abspath= os.path.join(os.path.dirname(os.path.abspath(os.path.join(__file__,"../../"))),"public")

def code_conversion(response):
    '''
    解决requests的编码问题
    :param response: requests库请求过来的响应体
    :return:
    '''
    html = response.content
    htmltxt = ''
    encode_type = chardet.detect(html)['encoding']
    if encode_type == None:
        try:
            htmltxt = gzip.decompress(html).decode('GB2312', 'ignore')
        except Exception as aa:
            print(aa)
            print('使用压缩文件转换编码时出现了问题')
    else:
        try:
            htmltxt = response.content.decode(str(encode_type), 'ignore')
        except Exception as ee:
            print(ee)
            print('编码格式出现了问题，需要转换的编码为', encode_type)
    return htmltxt

def download_load2(url, filepath, name):
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    filename = os.path.join(filepath, name)
    print(filename, '开始下载')
    try:
        with open(filename, 'wb')as fp:
            fp.write(requests.get(url).content)
            print(filename+"下载成功")
            fp.close()
    except Exception as e:
        print(filename+'下载失败！！！！！！！！！！！', e)
    return filename
    pass
def download_load(url, filepath, name):
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    filename = os.path.join(filepath, name)
    if os.path.exists(filename):
        return filename
    print(filename, '开始下载')
    try:
        with open(filename, 'wb')as fp:
            fp.write(requests.get(url).content)
            print(filename+"下载成功")
            fp.close()
    except Exception as e:
        print(filename+'下载失败！！！！！！！！！！！', e)
    return filename
    pass

def listdir(path, list_name):  # 传入存储的list
    print(path, os.listdir(path))
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            listdir(file_path, list_name)
        else:
            list_name.append(file_path)


def dirStart(isLoad):
    list = []
    if isLoad or len(list) <= 0:
        listdir("./images/", list)
    print(os.path.abspath(list[random.randint(0, len(list)-1)]))

    pass
# dirStart(False)


def listdir(path, list_name):  # 传入存储的list
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            listdir(file_path, list_name)
        else:
            print(file_path)
            list_name.append(file_path)
            # fsize = os.path.getsize(file_path)
            # if fsize<=0:
            #     print('删除损坏文件：',file_path)
            #     os.remove(file_path)
filePathList = []

def randomFile2(isLoad):
    global filePathList
    if isLoad or len(filePathList) <= 0:
        filePathList = []
        global abspath
        if abspath != "":
            filePath = abspath+"/"
        else:
            abspath = "./images/"
        listdir(abspath, filePathList)

    filePath = os.path.abspath(
        filePathList[random.randint(0, len(filePathList)-1)])
    print('随机到图片===>', filePath)
    return filePath

def randomFile(isLoad):  # 传入存储的list
    global abspath
    if abspath != "":
        filePath = abspath+"/"
    else:
        abspath = "./images/"
    for i in [0,1,2,3,4]:
        result=getRandomFile(abspath)
        if result:
            return result
        else:
            continue

def getRandomFile(path):
   files= os.listdir(path)
   #print(files)
   if files:
    file=files[random.randint(0, len(files)-1)]
    file_path = os.path.join(path, file)
    print(file_path)
    if os.path.isdir(file_path):
        return getRandomFile(file_path)
    else:
        return file_path
   else:
    return None
   
#randomFile(True)

