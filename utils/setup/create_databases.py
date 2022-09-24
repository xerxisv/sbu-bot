from pathlib import Path

from sqlite3 import connect

from utils.schemas import BannedMember, InactivePlayerSchema, RepCommandSchema, SchemaAbstract, SuggestionSchema, \
    VerifiedMemberSchema

databases = [
    SuggestionSchema.Suggestion,
    InactivePlayerSchema.InactivePlayer,
    RepCommandSchema.RepCommand,
    VerifiedMemberSchema.VerifiedMember,
    BannedMember.BannedMember
]


def create_dbs():
    Path('./data').mkdir(parents=True, exist_ok=True)

    for db_schema in databases:
        db = connect(SchemaAbstract.Schema.DB_PATH + db_schema.DB_NAME + '.db')

        cursor = db.cursor()
        cursor.executescript(db_schema.create())

        db.commit()
        db.close()
