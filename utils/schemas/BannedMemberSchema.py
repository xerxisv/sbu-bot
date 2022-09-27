import time
from typing import TypedDict

from aiosqlite import Row

from utils.schemas import Schema


class BannedMemberInfo(TypedDict):
    uuid: str
    reason: str
    moderator: int
    banned_at: int
    message: int


class BannedMember(Schema):
    DB_NAME = 'banned-list'

    def __init__(self, uuid: str, reason: str, moderator: int):
        self.uuid = uuid
        self.reason = reason
        self.moderator = moderator

    def insert(self) -> (str, dict):
        return '''
            INSERT
            INTO BANNED (uuid, reason, moderator, created_at)
            VALUES (:uuid, :reason, :moderator, :created_at)
        ''', {
            "uuid": self.uuid,
            "reason": self.reason,
            "moderator": self.moderator,
            "created_at": int(time.time())
        }

    def insert_msg(self, msg: int) -> str:
        return f'''
            UPDATE BANNED
            SET "message"={msg}
            WHERE uuid='{self.uuid}'
        '''

    @staticmethod
    def create() -> str:
        return '''
            CREATE TABLE IF NOT EXISTS "BANNED" (
                "uuid" TEXT PRIMARY KEY ,
                "reason" TEXT DEFAULT 'None',
                "moderator" INTEGER NOT NULL,
                "created_at" INTEGER NOT NULL,
                "message" INTEGER DEFAULT NULL
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
    def delete_row_with_id(_id: str) -> str:
        return f'''
            DELETE
            FROM BANNED
            WHERE uuid='{_id}'
        '''

    @staticmethod
    def dict_from_tuple(query_res: Row) -> BannedMemberInfo:
        return {
            "uuid": query_res[0],
            "reason": query_res[1],
            "moderator": query_res[2],
            "banned_at": query_res[3],
            "message": query_res[4]
        }
