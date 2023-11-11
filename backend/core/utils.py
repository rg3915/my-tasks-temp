import sys
from datetime import datetime, timedelta

from faker import Faker

fake = Faker()


def progressbar(it, prefix="", size=60, file=sys.stdout):
    count = len(it)

    def show(j):
        x = int(size * j / count)
        file.write("%s[%s%s] %i/%i\r" %
                   (prefix, "#" * x, "." * (size - x), j, count))
        file.flush()
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i + 1)
    file.write("\n")
    file.flush()


def gen_short_title():
    return fake.sentence(nb_words=3).replace('.', '')


def gen_title():
    return fake.sentence()


def gen_phrase(n=5):
    return ' '.join(fake.texts(nb_texts=n))


def gen_name():
    return fake.first_name()


def gen_company():
    return fake.company()


def datetime_to_string(value, format='%Y-%m-%d %H:%M:%S'):
    '''
    Transforma datetime em string no formato %Y-%m-%d %H:%M:%S.
    '''
    return value.strftime(format)


def timedelta_to_string(value, format='%H:%M:%S'):
    total_seconds = value.total_seconds()
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if value.microseconds:
        format_with_seconds = format + ':%f'
        value_with_microseconds = timedelta(hours=hours, minutes=minutes, seconds=seconds, microseconds=value.microseconds)  # noqa E501
        return datetime.strftime(datetime.strptime(str(value_with_microseconds), '%H:%M:%S.%f'), format_with_seconds)[:-3]  # noqa E501
    else:
        # format_without_seconds = format
        return f"{int(hours):02d}:{int(minutes):02d}"
