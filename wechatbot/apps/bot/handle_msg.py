import re
from django import views
import requests
import os
import json
from queue import Queue
from .models import *
import time
bot_wx_info=None
def handle_msg(wx_obj, msg):
    global bot_wx_info
    if not bot_wx_info:
        bot_wx_info= wx_obj.get_self_info()
    bot_wxid=bot_wx_info['wx_id']
    bot_nick_name=bot_wx_info['nick_name']
    ## msg对象信息
    # msg_type	消息类型(1文本消息,3图片消息,34语音消息,37好友请求,40可能是好友消息,42个人名片,43视频消息,47自定义表情包,48位置消息,49共享实时位置、等xml消息,50未知消息,51微信初始化消息,52未知消息,53未知消息,62小视频消息,490微信转账,491邀请进群,492卡片链接,493文件,494小程序,666撤回消息,9999未知消息,10002提现消息,10000系统消息)
    # wx_id	来源ID(19162403962@chatroom)
    # wx_account	微信账号，如果不是好友的消息则为空
    # content	消息内容
    # self_wx_id	接收者微信ID
    # sender	如果是群消息，该参数为发送者的微信ID，否则为空
    # file_path	消息文件路径
    # is_self_msg	True：自己发送的消息，False：他人发送的消息
    # detail	详情参数，特定类型才有该值
    if msg['sender']  :
        #群消息
        handle_group_message(wx_obj,message=msg)
    else:
        #好友消息
        handle_single_message(wx_obj,message=msg)
    pass
#好友消息
def handle_single_message(wx_obj, message):
    print("处理【好友】消息===>", message)
    from_chatroom_wxid = message["wx_id"]  # 来自群组id
    msg_content =message["content"]  # 消息内容
    back_msg=None
    #智能聊天
    back_msg=bot_chat(bot_wx_info['nick_name'],msg_content,False)
    if back_msg:
        wx_obj.send_text(bot_wx_info['wx_id'],from_chatroom_wxid, back_msg)

 #群消息处理
def handle_group_message(wx_obj, message):
    print("处理【群组】消息===>", message)
    from_chatroom_wxid = message["wx_id"]  # 来自群组id
    msg_content =message["content"]  # 消息内容
    from_wxid = message["sender"]  # 发送消息的用户id
    back_msg=None

    print(from_chatroom_wxid,msg_content,from_wxid)
    #智能聊天
    back_msg=bot_chat(bot_wx_info['nick_name'],msg_content,True)
    if back_msg:
        wx_obj.send_text(bot_wx_info['wx_id'],from_chatroom_wxid, back_msg)
#机器人聊天
def bot_chat(bot_name,msg_content,isGroup):
    print('聊天内容：',bot_name,msg_content,isGroup)
    response=None
    if isGroup :
        if re.match(r'.*@'+bot_name+'\\u2005.*', msg_content):
            msg_content =re.match( r'(.*)@'+bot_name+'\\u2005.*', msg_content).group(1)+re.match( r'.*@'+bot_name+'\\u2005(.*)', msg_content).group(1)
            print('【群组】@我的消息处理后：',msg_content)
            response = requests.get("http://api.qingyunke.com/api.php?key=free&appid=0&msg="+msg_content)
    else:
        response = requests.get("http://api.qingyunke.com/api.php?key=free&appid=0&msg="+msg_content)
    if response:
        print(response.text)
        return json.loads(response.text).get('content','').replace('{br}','\n')
    return ''