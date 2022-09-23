from typing import TypedDict

from .SchemaAbstract import Schema

class GuildTatsuInfo(TypedDict):
    discord_id: int
    tatsu: int

class GuildTatsu(Schema):
    DB_NAME="gtatsu"

    def __init__(self, discord_id: int, tatsu: int):
        self.discord_id = discord_id
        self.tatsu = tatsu
    
    def insert(self) -> str:
        return f'''
					INSERT OR REPLACE INTO "GTATSU"
                    VALUES ({self.discord_id}, {self.tatsu})
                '''
        
    @staticmethod
    def create() -> str:
        return f'''
                    CREATE TABLE IF NOT EXISTS "GTATSU" (
                        discord_id INTEGER PRIMARY KEY,
                        tatsu INTEGER NOT NULL
                    )
                '''
            
    @staticmethod
    def select_row_with_id(_id: int) -> str:
        return f'''
			SELECT *
			FROM "GTATSU"
            WHERE "discord_id" = {_id};
        '''
    
    @staticmethod
    def dict_from_tuple(query_res) -> GuildTatsuInfo:
        if query_res is not None:
            res = {
                "discord_id": query_res[0],
                "tatsu": query_res[1]
            }
        else:
            res = {
                "discord_id": 0,
                "tatsu": 0
            }
        return res