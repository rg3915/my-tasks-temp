from django import forms

from .models import Issue, Milestone, Task


class IssueForm(forms.ModelForm):

    class Meta:
        model = Issue
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['x-model'] = f'editItem.{field_name}'


class MilestoneForm(forms.ModelForm):

    class Meta:
        model = Milestone
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['x-model'] = f'editItem.{field_name}'


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['x-model'] = f'editItem.{field_name}'
