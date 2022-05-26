
### 项目说明
通过API远程操作PC微信客户端发送微信消息、获取好友、群聊信息，以及通过Python调用微信获取好友、群、公众号列表，并收发消息，在线发送消息等。
- 基于[WeChatPYAPI项目](https://github.com/mrsanshui/WeChatPYAPI)的web实现


  
### 环境说明
- 需要windows环境，python3.7 , 微信WeChatSetup 3.3.0.115
- 安装文件下载地址：https://www.aliyundrive.com/s/9t6HztfYn7B 密码：hv60
- 项目启动：
```
#初始化
pip install -r requirements.txt
#启动项目
python manage.py runserver 0.0.0.0:8000
```
- http://localhost:8000/admin/ 管理地址
- 默认账号/密码wechatbot/wechatbot
 
### 功能支持
- python本地操作功能
  - 登录
  - 获取登录信息
  - 退出微信登录
  - 拉取好友/群/公众号列表
  - 获取群成员列表
  - 发送文本消息
  - 发送图片消息
  - 发送卡片链接
  - 接收微信消息
  - 收款
  - 退款
```
    #拉取列表（好友/群/公众号等）第一次拉取可能会阻塞，可以自行做异步处理
    # 好友列表：pull_type = 1
    # 群列表：pull_type = 2
    # 公众号列表：pull_type = 3
    # 其他：pull_type = 4
    lists = wx_obj.pull_list(self_wx=self_wx, pull_type=1)
    print(lists)

    # 获取群成员列表
    # lists = wx_obj.get_chat_room_members(self_wx=self_wx, to_chat_room="123456789@chatroom")
    # print(lists)

    # 发送文本消息
    wx_obj.send_text(self_wx=self_wx, to_wx="filehelper", msg='hello world')
    time.sleep(1)

    # 发送图片消息
    # wx_obj.send_img(self_wx=self_wx, to_wx="filehelper", path=r"C:\hello.png")
    # time.sleep(1)

    # 发送卡片链接
    wx_obj.send_card_link(
        self_wx=self_wx,
        to_wx="filehelper",
        title="hello world!",
        desc="世界你好，print('hello world!')",
        target_url="https://baike.baidu.com/item/hello%20world/85501",
        img_url="https://bkimg.cdn.bcebos.com/pic/3b87e950352ac65cd20ecfcbf9f2b21193138a7b?x-bce-process=image/resize,m_lfit,w_536,limit_1/format,f_jpg"
    )

```
- api远程操作功能
  - 登录api
  - 获取登录信息api
  - 退出微信登录api
  - 获取好友/群/公众号列表api
  - 获取群成员列表api
  - 发送文本消息api
  - 发送图片消息api
  - 发送卡片链接api
- api列表
  ![api列表](https://github.com/terrywangt/PublicFile/blob/master/Markdown/wechatbot_apilist.png?raw=true "api列表")
- [ApiFox在线接口文档](https://www.apifox.cn/web/project/1033501)

### 聊天演示
##### 好友聊天

  ![好友聊天](https://github.com/terrywangt/PublicFile/blob/master/Markdown/wechatbot_friend.jpg?raw=true "好友聊天")
##### 群聊天

  ![群聊天](https://github.com/terrywangt/PublicFile/blob/master/Markdown/wechatbot_group.jpg?raw=true "群聊天")
### 声明
- 本项目仅供技术研究，请勿用于非法用途，如有任何人凭此做何非法事情，均于作者无关，特此声明。
