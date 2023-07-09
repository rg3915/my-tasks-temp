from django.contrib import admin

from .models import Issue, Label, Milestone, Tag, Task


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('tag',)


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('label',)


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('title',)


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'milestone', 'status')
    readonly_fields = ('slug',)
    search_fields = ('title',)
    list_filter = ('status', 'labels', 'milestone')
    date_hierarchy = 'created'


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'project', 'issue', 'status', 'start_time', 'end_time')
    readonly_fields = ('slug',)
    search_fields = ('title',)
    list_filter = ('status', 'tags')
    date_hierarchy = 'created'
