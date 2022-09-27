from typing import TypedDict
import time

from utils.schemas.SchemaAbstract import Schema


class VerifiedMemberInfo(TypedDict):
    discord_id: int
    uuid: str
    guild_uuid: str


class VerifiedMember(Schema):

    DB_NAME = 'verified'

    def __init__(self, discord_id: int, uuid: str, guild_uuid: str = None):
        self.discord_id = discord_id
        self.uuid = uuid
        self.guild_uuid = guild_uuid

    def insert(self) -> (str, dict):
        return '''
            INSERT OR REPLACE INTO "VERIFIED"
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
            CREATE TABLE IF NOT EXISTS "VERIFIED" (
            "discord_id" INTEGER PRIMARY KEY , 
            "uuid" TEXT UNIQUE ,
            "guild_uuid" TEXT ,
            "created_at" INTEGER NOT NULL 
            );
        '''

    @staticmethod
    def delete_row_with_id(_id: int):
        return f'''
            DELETE
            FROM "VERIFIED"
            WHERE discord_id={_id}
        '''

    @staticmethod
    def select_row_with_id(_id: int) -> str:
        return f'''
            SELECT *
            FROM "VERIFIED"
            WHERE discord_id={_id}
        '''
    
    @staticmethod
    def update_rows(_ids: tuple):
        return f'''
            UPDATE "VERIFIED"
            SET "guild_uuid"=NULL
            WHERE "uuid" IN {_ids}
        '''
    
    @staticmethod
    def select_row_with_guild_uuid(_id: str) -> str:
        return f'''
            SELECT *
            FROM "VERIFIED"
            WHERE "guild_uuid"='{_id}'
        '''
    
    @staticmethod
    def select_all() -> str:
        return '''
            SELECT *
            FROM "VERIFIED"
        '''

    @staticmethod
    def dict_from_tuple(query_res) -> VerifiedMemberInfo:
        return {
            'discord_id': query_res[0],
            'uuid': query_res[1],
            'guild_uuid': query_res[2]
        }
