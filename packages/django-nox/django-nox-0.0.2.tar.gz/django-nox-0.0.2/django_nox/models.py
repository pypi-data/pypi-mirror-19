# coding=utf-8
from __future__ import unicode_literals

from django.db import models


class LoadTimeLog(models.Model):
    method = models.CharField(max_length=64, verbose_name='调用方法')
    query = models.TextField(verbose_name='请求参数', default='')
    code = models.PositiveIntegerField(verbose_name='请求状态')
    url = models.CharField(max_length=512, verbose_name='请求地址')
    sql = models.TextField(verbose_name='执行sql')
    load_time = models.DecimalField(max_digits=7, decimal_places=4, verbose_name='请求时间')
    sql_time = models.DecimalField(max_digits=7, decimal_places=4, verbose_name='sql耗时')
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'django_nox_loadtimelog'


