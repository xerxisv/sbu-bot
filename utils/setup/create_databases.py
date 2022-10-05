from sqlite3 import connect

from utils.database.schemas import BannedMember, InactivePlayer, RepCommand, Schema, Suggestion, \
    VerifiedMember

databases = [
    Suggestion,
    InactivePlayer,
    RepCommand,
    VerifiedMember,
    BannedMember
]


def create_dbs():
    db = connect(Schema.DB_PATH)

    for db_schema in databases:
        cursor = db.cursor()
        cursor.executescript(db_schema.create())

    db.commit()
    db.close()
