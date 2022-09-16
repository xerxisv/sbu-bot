from typing import TypedDict
from .SchemaAbstract import Schema
import time


class RepCommandInfo(TypedDict):
	rep_id: int
	receiver: int
	provider: int
	reason: str
	message: int


class RepCommand(Schema):
	DB_NAME = 'reputation'

	def __init__(self, rep_id: int, receiver: int, provider: int, reason: str):
		self.rep_id = rep_id
		self.receiver = receiver
		self.provider = provider
		self.reason = reason

	def insert(self) -> (str, dict):
		return '''
			INSERT INTO "REP-COMMANDS" ("rep-id", receiver, provider, reason, created_at)
			VALUES (:rep_id, :receiver, :provider, :reason, :created_at)
		''', {
			"rep_id": self.rep_id,
			"receiver": self.receiver,
			"provider": self.provider,
			"reason": self.reason,
			"created_at": int(time.time())
		}

	def count_reps(self) -> str:
		return f'''
			SELECT COUNT("receiver"={self.receiver})
			FROM "REP-COMMANDS";
		'''

	def set_message(self, msg_id: int) -> str:
		return f'''
		UPDATE "REP-COMMANDS"
		SET "message"={msg_id}
		WHERE "rep-id"={self.rep_id};
		'''

	@staticmethod
	def dict_from_tuple(query_res) -> RepCommandInfo:
		return {
			'rep_id': query_res[0],
			'receiver': query_res[1],
			'provider': query_res[2],
			'reason': query_res[3],
			'message': query_res[4],
		}

	@staticmethod
	def select_row_with_id(_id: int) -> str:
		return f'''
			SELECT *
			FROM "REP-COMMANDS"
			WHERE "rep-id"={_id};
		'''

	@staticmethod
	def delete_row_with_id(_id: int) -> str:
		return f'''
			DELETE 
			FROM "REP-COMMANDS"
			WHERE "rep-id"={_id}
		'''

	@staticmethod
	def create() -> str:
		return '''
			CREATE TABLE IF NOT EXISTS "REP-COMMANDS" (
				"rep-id" INTEGER PRIMARY KEY , 
				"receiver" INTEGER NOT NULL ,
				"provider" INTEGER NOT NULL ,
				"reason" TEXT NOT NULL ,
				"message" INTEGER DEFAULT null ,
				"created_at" INTEGER NOT NULL 
			);
		'''

	@staticmethod
	def count_rows() -> str:
		"""

		:return: Query string to count the number of rows contained in the SUGGESTIONS table
		"""
		return 'SELECT COUNT(*) FROM "REP-COMMANDS";'

	@staticmethod
	def get_max_rep_id() -> str:
		return '''
		SELECT max("rep-id")
		FROM "REP-COMMANDS"
		'''
