from pathlib import Path

from aiosqlite import connect

from utils.schemas import BannedMember, InactivePlayerSchema, RepCommandSchema, SchemaAbstract, SuggestionSchema, \
    VerifiedMemberSchema, GuildTatsuSchema

databases = [
    GuildTatsuSchema.GuildTatsu,
    SuggestionSchema.Suggestion,
    InactivePlayerSchema.InactivePlayer,
    RepCommandSchema.RepCommand,
    VerifiedMemberSchema.VerifiedMember,
    BannedMember.BannedMember
]


async def create_dbs():
    Path('./data').mkdir(parents=True, exist_ok=True)

    for db_schema in databases:
        db = await connect(SchemaAbstract.Schema.DB_PATH + db_schema.DB_NAME + '.db')

        cursor = await db.cursor()
        await cursor.executescript(db_schema.create())

        await db.commit()
        await db.close()
