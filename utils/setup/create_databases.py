from sqlite3 import connect

from utils.schemas import BannedMember, InactivePlayer, RepCommand, Schema, Suggestion, \
    VerifiedMember

databases = [
    Suggestion,
    InactivePlayer,
    RepCommand,
    VerifiedMember,
    BannedMember
]


def create_dbs():
    for db_schema in databases:
        db = connect(Schema.DB_PATH + db_schema.DB_NAME + '.db')

        cursor = db.cursor()
        cursor.executescript(db_schema.create())

        db.commit()
        db.close()
