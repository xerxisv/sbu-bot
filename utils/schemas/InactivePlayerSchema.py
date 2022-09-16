import time

from .SchemaAbstract import Schema

from utils.constants import GUILDS_INFO


class InactivePlayer(Schema):
	DB_NAME = 'inactive'

	def __init__(self, discord_id: int, uuid: str, guild_uuid: str, inactive_until: int):
		self.discord_id = discord_id
		self.uuid = uuid
		self.guild_uuid = guild_uuid
		self.inactive_until = inactive_until

	def insert(self) -> (str, dict):
		return f'''
					INSERT OR REPLACE INTO "INACTIVES"
					VALUES (:discord_id , :uuid, :guild_uuid, :inactive_until, :created_at)
				''', {
					"discord_id": self.discord_id,
					"uuid": self.uuid,
					"guild_uuid": self.guild_uuid,
					"inactive_until": self.inactive_until,
					"created_at": int(time.time())
				}

	@staticmethod
	def create() -> str:
		create_string = '''
				CREATE TABLE IF NOT EXISTS "INACTIVES" (
					discord_id INTEGER PRIMARY KEY ,
					uuid text UNIQUE NOT NULL ,
					guild_uuid text NOT NULL ,
					inactive_until INTEGER NOT NULL ,
					created_at INTEGER NOT NULL 
				);
				
		'''
		for index, guild_name in enumerate(GUILDS_INFO.keys()):
			create_string += f'''
				INSERT OR REPLACE INTO INACTIVES
				VALUES ({index}, '{GUILDS_INFO[guild_name]['bridge_uuid']}', '{GUILDS_INFO[guild_name]['guild_uuid']}',
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
			SELECT ()
			FROM INACTIVES
			WHERE discord_id={_id}
		'''
