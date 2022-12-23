from itertools import chain
from django.contrib import admin
from webapp.models import IssueModel, TypeModel, StatusModel, ProjectModel


# Register your models here.
class IssueAdmin(admin.ModelAdmin):
    def type_name(self, obj):
        a = obj.type.values_list('title')
        return list(chain.from_iterable(a))

    list_display = ['id', 'title', 'status', 'type_name', 'content', 'created_at', 'project']
    list_display_links = ['title']
    list_filter = ['title']
    search_fields = ['title', 'content']
    fields = ['title', 'status', 'type', 'content', 'created_at', 'updated_at', 'project']
    readonly_fields = ['created_at', 'updated_at']


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content', 'created_at', 'updated_at']
    list_display_links = ['title']
    list_filter = ['title']
    fields = ['title', 'content', 'users', 'created_at', 'updated_at']


class TypeAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_display_links = ['title']
    list_filter = ['title']
    search_fields = ['title']
    fields = ['title']


class StatusAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_display_links = ['title']
    list_filter = ['title']
    search_fields = ['title']
    fields = ['title']


admin.site.register(IssueModel, IssueAdmin)
admin.site.register(TypeModel, TypeAdmin)
admin.site.register(StatusModel, StatusAdmin)
admin.site.register(ProjectModel, ProjectAdmin)