from collections import defaultdict
from datetime import timedelta


from backend.core.utils import datetime_to_string, get_hour_display
from backend.task.models import Timesheet


def group_by_date(project):
    """
    Agrupa os dados por dia.
    """
    timesheet_data = (
        Timesheet.objects.filter(task__project__title=project)
        .values(
            'start_time__date',
            'task__issue__number',
            'start_time',
            'end_time',
            'task__issue__sprint__number',
        )
        .order_by('start_time')
    )

    # Cria um dicionário para armazenar as horas totais e as issues por data.
    result_dict = defaultdict(lambda: {'total_hours': timedelta(), 'issues': set()})

    for timesheet in timesheet_data:
        start_time = timesheet.get('start_time')
        end_time = timesheet.get('end_time')

        total_hours = timedelta()
        if start_time is not None and end_time is not None:
            total_hours = end_time - start_time

        date_only = timesheet['start_time'].date()
        issues = timesheet['task__issue__number']
        result_dict[date_only]['total_hours'] += total_hours
        result_dict[date_only]['issues'].add(issues)
        result_dict[date_only]['sprint'] = timesheet['task__issue__sprint__number']

    output = [
        {
            'date': datetime_to_string(key, '%d/%m/%y'),
            'month': key.month,
            'total_hours': value['total_hours'],
            'total_hours_display': str(get_hour_display(value['total_hours'])),
            'issues': ', '.join(map(str, value['issues'])),
            'sprint': value['sprint'],
        }
        for key, value in result_dict.items()
    ]

    return output


def group_data(project, group_by_field, key_field):
    timesheet_data = (
        Timesheet.objects.filter(task__project__title=project)
        .values('start_time', 'end_time', group_by_field)
        .order_by('start_time')
    )

    # Cria um dicionário para armazenar as horas totais e as issues por data.
    result_dict = defaultdict(lambda: {'total_hours': timedelta(), 'issues': set()})

    for timesheet in timesheet_data:
        # Agrupa pelo campo definido em group_by_field.
        date_only = timesheet[group_by_field]

        start_time = timesheet.get('start_time')
        end_time = timesheet.get('end_time')

        total_hours = timedelta()
        if start_time is not None and end_time is not None:
            total_hours = end_time - start_time

        result_dict[date_only]['total_hours'] += total_hours

    output = [
        {
            key_field: key,
            'total_hours': value['total_hours'],
            'total_hours_display': str(get_hour_display(value['total_hours'])),
        }
        for key, value in result_dict.items()
    ]

    return output


def group_by_month(project):
    """
    Agrupa os dados por mês.
    """
    return group_data(project, 'start_time__month', 'month')


def group_by_sprint(project):
    """
    Agrupa os dados por sprint.
    """
    return group_data(project, 'task__issue__sprint__number', 'sprint')
