import time

from utils.schemas import Schema

from utils.constants import GUILDS_INFO

from typing import TypedDict


class InactivePlayerInfo(TypedDict):
	uuid: str
	discord_id: int
	guild_uuid: str
	inactive_until: int
	created_at: int


class InactivePlayer(Schema):
	DB_NAME = 'inactive'
	LIMIT = 10

	def __init__(self, uuid: str, discord_id: int, guild_uuid: str, inactive_until: int):
		self.uuid = uuid
		self.discord_id = discord_id
		self.guild_uuid = guild_uuid
		self.inactive_until = inactive_until

	def insert(self) -> (str, dict):
		return f'''
					INSERT OR REPLACE INTO INACTIVES
					VALUES (:uuid, :discord_id, :guild_uuid, :inactive_until, :created_at);
				''', {
					"uuid": self.uuid,
					"discord_id": self.discord_id,
					"guild_uuid": self.guild_uuid,
					"inactive_until": self.inactive_until,
					"created_at": int(time.time())
				}

	@staticmethod
	def create() -> str:
		create_string = '''
				CREATE TABLE IF NOT EXISTS INACTIVES (
					uuid text PRIMARY KEY ,
					discord_id INTEGER ,
					guild_uuid text NOT NULL ,
					inactive_until INTEGER NOT NULL ,
					created_at INTEGER NOT NULL 
				);
				
		'''
		for guild_name in GUILDS_INFO.keys():
			create_string += f'''
				INSERT OR REPLACE INTO INACTIVES
				VALUES ('{GUILDS_INFO[guild_name]['bridge_uuid']}', 0, '{GUILDS_INFO[guild_name]['guild_uuid']}',
				{int(time.time()) + 31556926}, {int(time.time())});
				
			'''
		return create_string

	@staticmethod
	def delete_inactive() -> str:
		return f'''
			DELETE
			FROM INACTIVES
			WHERE inactive_until < {int(time.time())};
		'''

	@staticmethod
	def select_row_with_id(_id: int) -> str:
		return f'''
			SELECT *
			FROM INACTIVES
			WHERE uuid={_id};
		'''

	@staticmethod
	def delete_row_with_uuid(uuid: str) -> str:
		return f'''
			DELETE
			FROM INACTIVES
			WHERE uuid='{uuid}';
		'''

	@staticmethod
	def count_rows() -> str:
		return '''
			SELECT COUNT(1)
			FROM INACTIVES;
		'''

	@staticmethod
	def select_all_limit(page: int):
		return f'''
			SELECT *
			FROM INACTIVES
			WHERE discord_id!=0
			ORDER BY guild_uuid
			LIMIT {InactivePlayer.LIMIT}
			OFFSET {(page - 1) * InactivePlayer.LIMIT}
		'''

	@staticmethod
	def dict_from_tuple(res) -> InactivePlayerInfo:
		return {
			"uuid": res[0],
			"discord_id": res[1],
			"guild_uuid": res[2],
			"inactive_until": res[3],
			"created_at": res[4],
		}
