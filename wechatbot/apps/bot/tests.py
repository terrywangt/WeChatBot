from django.test import TestCase
from .WeChatPYAPI import WeChatPYApi

import time
import logging
from queue import Queue
import os

# Create your tests here.

# python manage.py test

# 当前目录路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


logging.basicConfig(level=logging.INFO)  # 日志器
msg_queue = Queue()  # 消息队列


def on_message(msg):
    """消息回调，建议异步处理，防止阻塞"""
    print(msg)
    msg_queue.put(msg)


def on_exit(wx_id):
    """退出事件回调"""
    print("已退出：{}".format(wx_id))


print(BASE_DIR)

# help(WeChatPYApi)
# 实例化api对象
w = WeChatPYApi(msg_callback=on_message, exit_callback=on_exit, logger=logging)

# 启动微信
w.start_wx()
# w.start_wx(path=os.path.join(BASE_DIR, "login_qrcode.png"))  # 保存登录二维码# 这里需要阻塞，等待获取个人信息
while not w.get_self_info():
    time.sleep(5)

my_info = w.get_self_info()
self_wx = my_info["wx_id"]
print("登陆成功！")
print(my_info)


# 处理消息回调
while True:
    msg = msg_queue.get()

    # 收款
    if msg["msg_type"] == 490:
        is_recv = msg["detail"]["is_recv"]
        if is_recv:
            # 收款
            w.collection(self_wx=self_wx, msg_data=msg)
            # 退款
            # w.refund(self_wx=self_wx, msg_data=msg)
