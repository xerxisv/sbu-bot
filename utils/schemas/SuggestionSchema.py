import time
from typing import TypedDict

from .SchemaAbstract import Schema


class SuggestionInfo(TypedDict):
	suggestion_number: int
	message_id: int
	author_id: int
	suggestion: str


class Suggestion(Schema):
	"""
	Represents a suggestion row/document to be added in the database
	"""

	DB_NAME = 'suggestions'

	def __init__(self, suggestion_number: int, message_id: int, suggestion: str, author_id: int):
		"""
		\
		:param suggestion_number: The unique number that represent a suggestion
		:param message_id: The snowflake ID of the embed created in #suggestions
		:param suggestion: The suggestion string
		:param author_id: The snowflake ID of the suggestion author
		"""
		self.suggestion_number = suggestion_number
		self.message_id = message_id
		self.suggestion = suggestion
		self.author_id = author_id

	def insert(self) -> (str, dict):
		"""
		\
		:return: Tuple containing insertion string and fields dictionary
		"""
		return '''
			INSERT INTO "SUGGESTIONS" (suggestion_number, message_id, suggestion, author_id, created_at)
			VALUES (:suggestion_number, :message_id, :suggestion, :author_id, :created_at)
			''', {
			"suggestion_number": self.suggestion_number,
			"message_id": self.message_id,
			"suggestion": self.suggestion,
			"author_id": self.author_id,
			"created_at": int(time.time())
		}

	@staticmethod
	def select_row_with_id(_id: int) -> str:
		"""
		\
		:param _id: the ID of the suggestion in the db
		:return: query string that returns the suggestion with the given ID when executed
		"""
		return f'''
			SELECT suggestion_number, message_id, author_id, suggestion
			FROM SUGGESTIONS
			WHERE suggestion_number={_id};
		'''

	@staticmethod
	def set_approved(suggestion_id: int, is_approved: bool, answered_by: int, reason: str = "") -> (str, dict):
		"""
		\
		:param suggestion_id: the ID of the suggestion in the db
		:param is_approved: whether the suggestion was approved or not
		:param answered_by: the administrator ID that approved/ denied the suggestion
		:param reason: reason of approval/ denial
		:return: tuple containing query string that updates the row with the new information and dict with query options
		"""
		return '''
			UPDATE "SUGGESTIONS"
			SET "answered"=:answered, "approved"=:approved, "reason"=:reason, "approved_by"=:approved_by
			WHERE "suggestion_number"=:suggestion_id
		''', {
			"answered": True,
			"approved": is_approved,
			"reason": reason,
			"approved_by": answered_by,
			"suggestion_id": suggestion_id,
		}

	@staticmethod
	def create() -> str:
		"""
		\
		:return: Table creation script
		"""
		return '''
				CREATE TABLE IF NOT EXISTS "SUGGESTIONS" (
					suggestion_number INTEGER PRIMARY KEY ,
					message_id INTEGER UNIQUE ,
					author_id INTEGER NOT NULL ,
					suggestion TEXT NOT NULL ,
					answered BOOLEAN DEFAULT false ,
					approved BOOLEAN DEFAULT false ,
					reason TEXT DEFAULT '' ,
					approved_by INTEGER DEFAULT null, 
					created_at INTEGER NOT NULL
				);
		'''

	@staticmethod
	def count_rows() -> str:
		"""

		:return: Query string to count the number of rows contained in the SUGGESTIONS table
		"""
		return 'SELECT COUNT(*) FROM "SUGGESTIONS";'

	@staticmethod
	def dict_from_tuple(query_res) -> SuggestionInfo:
		"""
		\
		:param query_res: the query response tuple fetched by the db cursor
		:return: a typed dictionary containing the response fields
		"""
		return {
			"suggestion_number": query_res[0],
			"message_id": query_res[1],
			"author_id": query_res[2],
			"suggestion": query_res[3]
		}
