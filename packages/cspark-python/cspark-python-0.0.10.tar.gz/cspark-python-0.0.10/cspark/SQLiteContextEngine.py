from collections import OrderedDict
import datetime
from peewee import CharField, Model, SqliteDatabase


db = SqliteDatabase('context_engine_cache.db')


class ContextInstance(Model):
    time = CharField(default=datetime.datetime.now)
    key = CharField()
    value = CharField(null=True)

    class Meta:
        database = db


class SQLiteContextEngine:

    def __init__(self):
        db.connect()

        if not ContextInstance.table_exists():
            db.create_tables([ContextInstance])

    def put_data(self, _key=None, _value=None):
        sorted_key = OrderedDict(sorted(_key.items(), key=lambda t: t[1]))
        ContextInstance(key=sorted_key, value=_value).save()

    def get_data(self, _key=None):
        sorted_key = OrderedDict(sorted(_key.items(), key=lambda t: t[1]))
        try:
            return ContextInstance.get(key=sorted_key)
        except ContextInstance.DoesNotExist:
            return None
