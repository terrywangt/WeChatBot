from concurrent.futures import thread
from xmlrpc.client import Boolean
from django.shortcuts import render
import logging
from os import path
import re
import time
import requests
import json
import logging
from django.http import HttpResponse,response
from .get_images import download_load
import threading,ctypes,inspect
import os
from .handle_msg import handle_msg
from .WeChatPYAPI import WeChatPYApi
# Create your views here.
logging.basicConfig(level=logging.INFO)  # 日志器
BASE_DIR = os.path.dirname(os.path.abspath(os.path.join(__file__,"../../")))
wx_obj = None
self_wx= None

def on_message(msg):
    """消息回调，建议异步处理，防止阻塞"""
    handle_msg(wx_obj,msg)
def on_exit(wx_id):
    """退出事件回调"""
    print("已退出：{}".format(wx_id))

class AwaitLoginThread(threading.Thread):
    def __init__(self, wx_obj):
        super(AwaitLoginThread, self).__init__()
        self.wx_obj = wx_obj
    def run(self):
        while not self.wx_obj.get_self_info():
            time.sleep(5)
        print('微信登录成功！')
# 启动登录
def start(request):
    try: 
        global wx_obj
        qrcode=request.GET.get('qrcode')
        if not wx_obj:
            wx_obj = WeChatPYApi(msg_callback=on_message, exit_callback=on_exit, logger=logging)
        imagepath=os.path.join(BASE_DIR, "public/images","login_qrcode.png")
        if qrcode and qrcode!='0':
            print(imagepath)
            if os.path.exists(imagepath):
                os.remove(imagepath)
            wx_obj.start_wx(path=imagepath)  # 保存登录二维码
            time.sleep(2)
        else:
            wx_obj.start_wx()
        print('启动成功！')
        t=AwaitLoginThread(wx_obj=wx_obj)
        t.start()
        if qrcode and qrcode!='0':
            if os.path.exists(imagepath):
                time.sleep(2)
            with open(imagepath, 'rb') as f:
                image_data = f.read()
            return HttpResponse(image_data, content_type="image/png")
        else:
            return HttpResponse(json.dumps({"message": "启动成功", "errorCode": 0, "data": ""}, ensure_ascii=False))
    except Exception as e:
        print('发生错误：', e)
        return HttpResponse(json.dumps({"message": "出现了无法预料的错误：", "errorCode": 0, "data": ""}, ensure_ascii=False))
# 退出登录
def logout(request):
    if wx_obj:
        wx_obj.logout(self_wx=wx_obj.get_self_info().get('wx_id', ''))
    return HttpResponse(json.dumps({"message": "退出成功", "errorCode": 0, "data": ""}, ensure_ascii=False))
#获取登录信息
def get_login_info(request):
    bot_info = wx_obj.get_self_info()
    return HttpResponse(json.dumps({"message": "获取成功", "errorCode": 0, "data": bot_info}, ensure_ascii=False))
# 获取1好友/2群/3公众号列表api
def get_friend_list(request):
    # 好友列表：pull_type = 1
    # 群列表：pull_type = 2
    # 公众号列表：pull_type = 3
    # 其他：pull_type = 4
    pull_type = 1
    if request.GET.get('pull_type'):
        pull_type=int(request.GET.get('pull_type'))
    lists = wx_obj.pull_list(self_wx=wx_obj.get_self_info().get('wx_id', ''), pull_type=pull_type)
    return HttpResponse(json.dumps({"message": "获取成功", "errorCode": 0, "data": lists}, ensure_ascii=False))
# 获取群成员列表
def get_chat_room_members(request):
    lists = wx_obj.get_chat_room_members(self_wx=wx_obj.get_self_info().get('wx_id', ''), to_chat_room=request.GET.get('to_chat_room'))
    return HttpResponse(json.dumps({"message": "获取成功", "errorCode": 0, "data": lists}, ensure_ascii=False))
# 发送文本
def send_text(request):
    '''
     body json类型
     {"bot_wxid":"wxid_kkp102awseir22","to_user":"","msg":""}
    '''
    param=json.loads(request.body.decode())
    wx_obj.send_text(wx_obj.get_self_info()['wx_id'],param["to_user"], param["msg"])    
    return response.JsonResponse({"message": "文本消息发送成功", "errorCode": 0, "data":param },safe=False,json_dumps_params={'ensure_ascii': False}) 

# 发送卡片
def send_link_card(request):
    '''
     body json类型
     {"bot_wxid":"wxid_kkp102awseir22","to_user":"","title":"","desc":"","target_url":"","img_url":""}
    '''
    param=json.loads(request.body.decode())
    wx_obj.send_card_link(wx_obj.get_self_info()['wx_id'],param["to_user"], param["title"], param["desc"], param["target_url"], param["img_url"])    
    return response.JsonResponse({"message": "card发送成功！", "errorCode": 0, "data":param },safe=False,json_dumps_params={'ensure_ascii': False}) 

# 发送图片
def send_img(request):
    '''
     body json类型
     {"bot_wxid":"wxid_kkp102awseir22","to_user":"","img_url":""}
    '''
    param=json.loads(request.body.decode())
    fileName=re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])","",param["img_url"])
    if param["img_url"].split('/')[-1].count(".")>0:
        fileName=fileName+os.path.splitext(param["img_url"])[-1]
    else:
        fileName=fileName+".jpg"
    if os.path.exists(os.path.join("./wechatbot/public/images/send_img", fileName)):
        os.remove(os.path.join("./wechatbot/public/images/send_img", fileName))
    filePath=os.path.abspath(download_load(param["img_url"],"./wechatbot/public/images/send_img",fileName))
    wx_obj.send_img(wx_obj.get_self_info()['wx_id'],param["to_user"], filePath)
    return response.JsonResponse({"message": "img发送成功", "errorCode": 0, "data":param },safe=False,json_dumps_params={'ensure_ascii': False}) 
