from django.contrib import admin

from sjsapp import models

# Register your models here.

admin.site.site_header = '设计师后台管理系统'
admin.site.site_title = '设计师后台管理系统'
admin.site.index_title = '设计师后台管理系统'

# 展示数据表
admin.site.register(models.SJUser)
admin.site.register(models.SJTask)
admin.site.register(models.SJOrder)
admin.site.register(models.SJWork)


