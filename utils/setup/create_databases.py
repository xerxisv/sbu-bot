from sqlite3 import connect

from utils.database.schemas import BannedMember, RepCommand, Schema, Suggestion, \
    User

databases = [
    Suggestion,
    RepCommand,
    User,
    BannedMember
]


def create_dbs():
    db = connect(Schema.DB_PATH)

    for db_schema in databases:
        cursor = db.cursor()
        cursor.executescript(db_schema.create())

    db.commit()
    db.close()
