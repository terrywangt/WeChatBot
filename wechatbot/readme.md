
### django-admin基本命令操作
- 快速新建项目、新建表操作、更新表结构命令
```
//建应用，建sqlite表 操作参考（https://blog.csdn.net/weixin_44605462/article/details/90484429）
//创建应用 python manage.py startapp 参数：应用名称，目录
python manage.py startapp myapp  /wechatbot/apps/myapp
//迁移表
python manage.py makemigrations
//更改表
python manage.py migrate
```
