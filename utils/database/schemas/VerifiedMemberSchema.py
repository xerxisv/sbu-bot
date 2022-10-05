import time
from typing import TypedDict

from aiosqlite import Row

from utils.database.schemas import Schema


class VerifiedMemberInfo(TypedDict):
    discord_id: int
    uuid: str
    guild_uuid: str


class VerifiedMember(Schema):

    def __init__(self, discord_id: int, uuid: str, guild_uuid: str = None):
        self.discord_id = discord_id
        self.uuid = uuid
        self.guild_uuid = guild_uuid

    def insert(self) -> (str, dict):
        return '''
            INSERT OR REPLACE INTO "USERS"
            VALUES (:discord_id, :uuid, :guild_uuid, :created_at)
        ''', {
            "discord_id": self.discord_id,
            "uuid": self.uuid,
            "guild_uuid": self.guild_uuid,
            "created_at": int(time.time())
        }

    @staticmethod
    def create() -> str:
        return '''
            CREATE TABLE IF NOT EXISTS "USERS" (
            "uuid" TEXT PRIMARY KEY ,
            "discord_id" INTEGER ,
            "ign" TEXT ,
            "guild_uuid" TEXT DEFAULT null ,
            "inactive_until" INTEGER DEFAULT null ,
            "tatsu_score" INTEGER DEFAULT 0 ,
            "created_at" INTEGER NOT null 
            );
        '''

    @staticmethod
    def delete_row_with_id(_id: int):
        return f'''
            DELETE
            FROM "USERS"
            WHERE discord_id={_id}
        '''

    @staticmethod
    def delete_row_with_profile_uuid(uuid: str):
        return f'''
            DELETE
            FROM "USERS"
            WHERE uuid={uuid}
        '''

    @staticmethod
    def select_row_with_id(_id: int) -> str:
        return f'''
            SELECT *
            FROM "USERS"
            WHERE discord_id={_id}
        '''

    @staticmethod
    def select_row_with_uuid(uuid: str) -> str:
        return f'''
            SELECT *
            FROM "USERS"
            WHERE uuid={uuid}
        '''
    
    @staticmethod
    def update_rows_with_ids(uuids: list) -> str:
        return f'''
            UPDATE "USERS"
            SET "guild_uuid"=NULL
            WHERE "uuid" IN ({', '.join(uuid for uuid in uuids)})
        '''
    
    @staticmethod
    def select_rows_with_guild_uuid(uuid: str) -> str:
        return f'''
            SELECT *
            FROM "USERS"
            WHERE "guild_uuid"='{uuid}'
        '''
    
    @staticmethod
    def select_all() -> str:
        return '''
            SELECT *
            FROM "USERS"
        '''

    @staticmethod
    def dict_from_tuple(query_res: Row) -> VerifiedMemberInfo:
        return {
            'discord_id': query_res[0],
            'uuid': query_res[1],
            'guild_uuid': query_res[2]
        }
