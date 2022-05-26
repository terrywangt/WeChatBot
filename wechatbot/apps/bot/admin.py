from django.contrib import admin

# Register your models here.
from wechatbot.apps.bot import models
admin.site.register(models.BotConfig)
