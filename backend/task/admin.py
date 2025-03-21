from django.contrib import admin
from import_export import resources
from import_export.admin import ExportActionModelAdmin, ImportExportModelAdmin

from .forms import LabelForm
from .models import Issue, Label, Milestone, Sprint, Tag, Task, Timesheet


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('tag',)


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'color')
    search_fields = ('label',)
    form = LabelForm


class MilestoneResource(resources.ModelResource):
    class Meta:
        model = Milestone


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    resource_classes = (MilestoneResource,)
    list_display = ('__str__', 'original_id', 'project')
    search_fields = ('title',)
    list_filter = ('project',)


class IssueInline(admin.TabularInline):
    model = Issue
    extra = 0


class SprintResource(resources.ModelResource):
    class Meta:
        model = Sprint


@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    resource_classes = (SprintResource,)
    inlines = (IssueInline,)
    list_display = ('__str__', 'project')
    list_filter = ('project',)


class IssueResource(resources.ModelResource):
    class Meta:
        model = Issue


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    resource_classes = (IssueResource,)
    list_display = ('__str__', 'get_labels', 'milestone', 'sprint', 'status')
    readonly_fields = ('slug', 'created', 'modified')
    search_fields = ('number', 'title')
    list_filter = ('status', 'labels', 'milestone')
    list_editable = ('status',)
    date_hierarchy = 'created'

    @admin.display(description='labels')
    def get_labels(self, obj):
        return ','.join(obj.labels.values_list('label', flat=True))


class TimesheetInline(admin.TabularInline):
    model = Timesheet
    extra = 0


class TaskResource(resources.ModelResource):
    class Meta:
        model = Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    resource_classes = (TaskResource,)
    inlines = (TimesheetInline,)
    list_display = ('__str__', 'project', 'status', 'issue')
    readonly_fields = ('slug', 'created', 'modified')
    search_fields = ('title',)
    list_filter = ('status', 'tags', 'project')
    list_editable = ('status',)
    date_hierarchy = 'created'


class TimesheetResource(resources.ModelResource):
    class Meta:
        model = Timesheet


@admin.register(Timesheet)
class TimesheetAdmin(ImportExportModelAdmin, ExportActionModelAdmin):
    resource_classes = (TimesheetResource,)
    list_display = ('__str__', 'get_project', 'start_time', 'end_time', 'get_hour')
    readonly_fields = ('slug', 'created', 'modified')
    search_fields = ('task__title',)
    list_filter = ('task__project',)
    date_hierarchy = 'created'

    @admin.display(description='project')
    def get_project(self, obj):
        return obj.task.project
