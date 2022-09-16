import time

from typing import TypedDict

from utils.schemas.SchemaAbstract import Schema


class BannedMemberInfo(TypedDict):
    uuid: str
    reason: str
    moderator: int


class BannedMember(Schema):

    DB_NAME = 'banned-list'

    def __init__(self, uuid: str, reason: str, moderator: int):
        self.uuid = uuid
        self.reason = reason
        self.moderator = moderator

    def insert(self) -> (str, dict):
        return '''
            INSERT
            INTO BANNED
            VALUES (:uuid, :reason, :moderator, :created_at)
        ''', {
            "uuid": self.uuid,
            "reason": self.reason,
            "moderator": self.moderator,
            "created_at": int(time.time())
        }

    @staticmethod
    def create() -> str:
        return '''
            CREATE TABLE IF NOT EXISTS "BANNED" (
                "uuid" TEXT PRIMARY KEY ,
                "reason" TEXT DEFAULT 'None',
                "moderator" INTEGER NOT NULL,
                "created_at" INTEGER NOT NULL 
            )
        '''

    @staticmethod
    def select_row_with_id(_id: str) -> str:
        return f'''
            SELECT *
            FROM "BANNED"
            WHERE uuid='{_id}'
        '''

    @staticmethod
    def dict_from_tuple(query_res) -> BannedMemberInfo:
        return {
            "uuid": query_res[0],
            "reason": query_res[1],
            "moderator": query_res[2],
        }
