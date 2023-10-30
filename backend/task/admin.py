from django.contrib import admin

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


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'original_id', 'project')
    search_fields = ('title',)


class IssueInline(admin.TabularInline):
    model = Issue
    extra = 0


@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    inlines = (IssueInline,)
    list_display = ('__str__', 'project')
    list_filter = ('project',)


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'get_labels', 'milestone', 'sprint', 'status')
    readonly_fields = ('slug', 'created', 'modified')
    search_fields = ('title',)
    list_filter = ('status', 'labels', 'milestone')
    date_hierarchy = 'created'

    @admin.display(description='labels')
    def get_labels(self, obj):
        return ','.join(obj.labels.values_list('label', flat=True))


class TimesheetInline(admin.TabularInline):
    model = Timesheet
    extra = 0


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    inlines = (TimesheetInline,)
    list_display = ('__str__', 'project', 'issue', 'status')
    readonly_fields = ('slug', 'created', 'modified')
    search_fields = ('title',)
    list_filter = ('status', 'tags')
    date_hierarchy = 'created'


@admin.register(Timesheet)
class TimesheetAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'start_time', 'end_time', 'get_hour')
    readonly_fields = ('slug', 'created', 'modified')
    search_fields = ('task__title',)
    list_filter = ('task__project',)
    date_hierarchy = 'created'
