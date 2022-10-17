import time
from typing import TypedDict

from aiosqlite import Row

from utils.database.schemas import Schema


class UserInfo(TypedDict):
    uuid: str
    discord_id: int
    ign: str
    guild_uuid: str
    inactive: int
    tatsu: int
    created_at: int


class User(Schema):

    def __init__(self, uuid: str, discord_id: int, ign: str, guild_uuid: str = None):
        self.uuid = uuid
        self.discord_id = discord_id
        self.ign = ign
        self.guild_uuid = guild_uuid

    def insert(self) -> (str, dict):
        return '''
            INSERT OR REPLACE INTO "USERS"(uuid, discord_id, ign, guild_uuid, created_at)
            VALUES (:uuid, :discord_id, :ign, :guild_uuid, :created_at)
        ''', {
            "uuid": self.uuid,
            "discord_id": self.discord_id,
            "ign": self.ign,
            "guild_uuid": self.guild_uuid,
            "created_at": int(time.time())
        }

    @staticmethod
    def create() -> str:
        return f'''
            CREATE TABLE IF NOT EXISTS "USERS" (
            "uuid" TEXT PRIMARY KEY ,
            "discord_id" INTEGER ,
            "ign" TEXT ,
            "guild_uuid" TEXT DEFAULT null ,
            "inactive_until" INTEGER DEFAULT null ,
            "tatsu_score" INTEGER DEFAULT 0 ,
            "last_week_tatsu" INTEGER DEFAULT 0,
            "created_at" INTEGER NOT null 
            );
            
            INSERT OR REPLACE INTO "USERS" (uuid, discord_id, ign, guild_uuid, inactive_until, created_at)
            VALUES
            ('e3020a41a5c24597ad11a2348c46f815', 0, 'UniversityBot', '6111fcb48ea8c95240436c57', 
                {int(time.time() + 31556926 )}, {int(time.time())}),
            ('a42c79f6f60841c38ae6ee1bf2eb7d35', 0, 'AlphaPsisBridge', '604a765e8ea8c962f2bb3b7a', 
                {int(time.time() + 31556926 )}, {int(time.time())}),
            ('384248632f3942069a80327a94150f6d', 0, 'KappaEtasBridge', '607a0d7c8ea8c9c0ff983976', 
                {int(time.time() + 31556926 )}, {int(time.time())}),
            ('d35172fc9191404c9671532569b62585', 0, 'DeltaOmegaBridge', '608d91e98ea8c9925cdb91b7', 
                {int(time.time() + 31556926 )}, {int(time.time())}),
            ('c767caebf1da4039ad47be2f9b8a61c6', 0, 'AlphaPsisBridge', '60a16b088ea8c9bb7f6d9052', 
                {int(time.time() + 31556926 )}, {int(time.time())}),
            ('4e65ce7ae36e4c64907bc525b4aab845', 0, 'LambdaPiBridg', '6125800e8ea8c92e1833e851', 
                {int(time.time() + 31556926 )}, {int(time.time())}),
            ('87de0116d5834793a3f2ad0d99b4e8f2', 0, 'MastersBridge', '570940fb0cf2d37483e106b3', 
                {int(time.time() + 31556926 )}, {int(time.time())})
        '''
    
    @staticmethod
    def set_tatsu(ign: str, tatsu: int) -> str:
        return f'''
            UPDATE "USERS"
            SET tatsu_score={tatsu}
            WHERE ign='{ign}'
        '''
    
    @staticmethod
    def set_last_week_tatsu(ign: str, tatsu: int) -> str:
        return f'''
            UPDATE "USERS"
            SET "last_week_tatsu"={tatsu}
            WHERE ign='{ign}'
        '''

    @staticmethod
    def add_inactive(uuid: str, afk_time: int) -> str:
        return f'''
            UPDATE "USERS"
            SET inactive_until={afk_time}
            WHERE uuid='{uuid}'
        '''

    @staticmethod
    def remove_inactive(uuid: str) -> str:
        return f'''
            UPDATE "USERS"
            SET inactive_until=null
            WHERE uuid='{uuid}'
        '''

    @staticmethod
    def remove_inactives() -> str:
        return f'''
            UPDATE "USERS"
            SET inactive_until=null
            WHERE inactive_until<{int(time.time())}
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
    def select_row_with_ign(ign: str) -> str:
        return f'''
            SELECT *
            FROM "USERS"
            WHERE "ign"='{ign}'
        '''
    
    @staticmethod
    def select_all() -> str:
        return '''
            SELECT *
            FROM "USERS"
        '''
    
    @staticmethod
    def select_top_tatsu() -> str:
        return '''
            SELECT *
            FROM "USERS"
            WHERE "discord_id"!=0
            ORDER BY
                "tatsu_score" DESC
            '''

    @staticmethod
    def dict_from_tuple(query_res: Row) -> UserInfo:
        return {
            'uuid': query_res[0],
            'discord_id': query_res[1],
            'ign': query_res[2],
            'guild_uuid': query_res[3],
            'inactive_until': query_res[4],
            'tatsu_score': query_res[5],
            'weekly_tatsu_score': query_res[6],
            'this_week_tatsu_score': query_res[5] - query_res[6],
            'created_at': query_res[7]
        }
