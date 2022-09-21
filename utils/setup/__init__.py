from .create_json_files import create_files
from .create_databases import create_dbs


async def run_setup():
	await create_dbs()
	create_files()
