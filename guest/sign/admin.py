from django.contrib import admin
from sign.models import Event, Guest


# Register your models here.



class EventAdmin(admin.ModelAdmin):
    list_display = ['name','status','start_time','id']  #  字段名称的数组 define the column
    search_fields = ['name']
    list_filter = ['status']

class GuestAdmin(admin.ModelAdmin):
    list_display = ['realname','phone','sign','create_time','event']
    search_fields = ['realname','phone']   # 创建表字段的搜索器 可以设置搜索关键字匹配多个表字段
    list_filter = ['sign','event']          #创建字段过滤器



admin.site.register(Event, EventAdmin)   #用EventAdmin 选项注册Event模块
admin.site.register(Guest, GuestAdmin)