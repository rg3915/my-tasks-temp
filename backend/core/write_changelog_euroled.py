import subprocess
from datetime import datetime


def check_if_the_date_already_exists(filename):
    date_format = datetime.now().strftime('%Y-%m-%d')

    # Check if the date already exists in the file
    with open(filename, 'r') as file:
        file_contents = file.read()
        if date_format in file_contents:
            print("Date already exists in the file.")
        else:
            # Append the date to the file
            with open(filename, 'a') as file:
                file.write(f"\n## {date_format}\n\n")
            print(f"Date {date_format} added to the file {filename}.")

            subprocess.run(f'tail {filename}', shell=True)


def write_changelog():
    customer = '/home/regis/euroled'
    filename = f'{customer}/CHANGELOG.md'
    print(filename)

    check_if_the_date_already_exists(filename)


if __name__ == '__main__':
    write_changelog()
