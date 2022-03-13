import mongoengine as db


class Test(db.Document):
    name = db.string
