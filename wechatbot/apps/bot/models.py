from django.db import models

# Create your models here.
class BotConfig(models.Model):
    bot_wxid = models.CharField(max_length=255, default='', blank=False, verbose_name='机器人微信id')
    val_type = models.CharField(max_length=255, default='', blank=False, verbose_name='配置的值类型（string字符串,array数组,object对象）')
    key = models.CharField(max_length=255, default='', blank=False, verbose_name='配置唯一key')
    val = models.CharField(max_length=4000, default='', blank=False, verbose_name='值')
    desc = models.CharField(max_length=4000, default='', blank=False, verbose_name='配置描述')
    class Meta:
        db_table = 'bot_config'
        verbose_name = '机器人配置表'
        verbose_name_plural = verbose_name