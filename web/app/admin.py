from django.contrib import admin
from app.models import Staff, Machine, Process, MoldData, Statistics
# Register your models here.

class staffAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class machineAdmin(admin.ModelAdmin):
    list_display = ('id', 'no')

class processAdmin(admin.ModelAdmin):
    list_display = ('id', 'type')

class moldDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'staff', 'machine', 'process', 'mod_no')

class statisticsAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_time')

admin.site.register(Staff, staffAdmin)
admin.site.register(Machine, machineAdmin)
admin.site.register(Process, processAdmin)
admin.site.register(MoldData, moldDataAdmin)
admin.site.register(Statistics, statisticsAdmin)