from typing import TypedDict
from .SchemaAbstract import Schema
import time


class RepCommandInfo(TypedDict):
	rep_id: int
	receiver: int
	provider: int
	comments: str
	msg_id: int
	type: str


class RepCommand(Schema):
	DB_NAME = 'reputation'
	LIMIT = 10

	def __init__(self, rep_id: int, receiver: int, provider: int, comments: str, rep_type: str):
		self.rep_id = rep_id
		self.receiver = receiver
		self.provider = provider
		self.comments = comments
		self.type = rep_type

	def insert(self) -> (str, dict):
		return '''
			INSERT INTO "REP-COMMANDS" ("rep-id", receiver, provider, comments, created_at, type)
			VALUES (:rep_id, :receiver, :provider, :comments, :created_at, :type)
		''', {
			"rep_id": self.rep_id,
			"receiver": self.receiver,
			"provider": self.provider,
			"comments": self.comments,
			"created_at": int(time.time()),
			"type": self.type
		}

	def set_message(self, msg_id: int) -> str:
		return f'''
		UPDATE "REP-COMMANDS"
		SET "msg_id"={msg_id}
		WHERE "rep-id"={self.rep_id};
		'''

	@staticmethod
	def dict_from_tuple(query_res) -> RepCommandInfo:
		return {
			'rep_id': query_res[0],
			'receiver': query_res[1],
			'provider': query_res[2],
			'comments': query_res[3],
			'type': query_res[4],
			'msg_id': query_res[5],
		}

	@staticmethod
	def select_row_with_id(_id: int) -> str:
		return f'''
			SELECT "rep-id", receiver, provider, comments, type, msg_id
			FROM "REP-COMMANDS"
			WHERE "rep-id"={_id};
		'''

	@staticmethod
	def count_rows_with_receiver(_id: int) -> str:
		return f'''
			SELECT COUNT(1)
			FROM "REP-COMMANDS"
			WHERE receiver={_id}
		'''

	@staticmethod
	def select_rows_with_receiver(_id: int, page: int) -> str:
		return f'''
			SELECT "rep-id", receiver, provider, comments, type, msg_id
			FROM "REP-COMMANDS"
			WHERE receiver={_id}
			ORDER BY "rep-id"
			LIMIT {RepCommand.LIMIT}
			OFFSET {(page - 1) * RepCommand.LIMIT}
		'''

	@staticmethod
	def count_rows_with_provider(_id: int) -> str:
		return f'''
			SELECT COUNT(1)
			FROM "REP-COMMANDS"
			WHERE provider={_id}
		'''

	@staticmethod
	def select_rows_with_provider(_id: int, page: int) -> str:
		return f'''
			SELECT "rep-id", receiver, provider, comments, type, msg_id
			FROM "REP-COMMANDS"
			WHERE provider={_id}
			ORDER BY "rep-id"
			LIMIT {RepCommand.LIMIT}
			OFFSET {(page - 1) * RepCommand.LIMIT}
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
				"comments" TEXT NOT NULL ,
				"created_at" INTEGER NOT NULL ,
				"type" TEXT NOT NULL ,
				"msg_id" INTEGER DEFAULT null
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
