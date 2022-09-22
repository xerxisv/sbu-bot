from .create_json_files import create_files
from .create_databases import create_dbs


def run_setup():
	create_dbs()
	create_files()
