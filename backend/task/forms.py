from django import forms

from .models import Issue, Label, Milestone, Task


class LabelForm(forms.ModelForm):

    class Meta:
        model = Label
        fields = '__all__'
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
        }


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
    start_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(
            format='%H:%M:%S',
            attrs={
                'type': 'time',
            }),
        input_formats=('%H:%M:%S',),
    )
    end_time = forms.TimeField(
        required=False,
        widget=forms.TimeInput(
            format='%H:%M:%S',
            attrs={
                'type': 'time',
            }),
        input_formats=('%H:%M:%S',),
    )

    class Meta:
        model = Task
        fields = (
            'title',
            'project',
            'issue',
            'tags',
            'annotation',
            'start_time',
            'end_time',
            'estimate',
            'report',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields['issue'].queryset = Issue.objects.none()

        for field_name, field in self.fields.items():
            field.widget.attrs['x-model'] = f'editItem.{field_name}'
