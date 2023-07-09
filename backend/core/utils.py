import sys

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
