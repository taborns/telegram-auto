from django.contrib import admin

# Register your models here.

from auto import models

class ActionModelAdmin(admin.ModelAdmin):
    list_display = ('label',)
class TaskPackageModelAdmin(admin.ModelAdmin):
    list_display = ('number', 'price')

class TaskModelAdmin(admin.ModelAdmin):
    list_display = ('entity_ident', 'action', 'package', 'status')

admin.site.register(models.Action, ActionModelAdmin)
admin.site.register(models.TaskPackage, TaskPackageModelAdmin)
admin.site.register(models.Task, TaskModelAdmin)