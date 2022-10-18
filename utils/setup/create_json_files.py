from os import path

FILES = ['qotd.json']


def create_files():
    for file in FILES:
        file_path = f'./data/{file}'
        if path.isfile(file_path):
            continue

        with open(file_path, 'x+') as f:
            f.write('[]')
