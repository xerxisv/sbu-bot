from .create_databases import create_dbs
from .create_json_files import create_files


def run_setup():
    create_dbs()
    create_files()
