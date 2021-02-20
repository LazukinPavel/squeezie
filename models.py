import shortuuid
from datetime import datetime

from peewee import Model, CharField, DateTimeField, IntegerField, DatabaseProxy

db = DatabaseProxy()


class Url(Model):
    class Meta:
        database = db

    uuid = CharField(default=shortuuid.ShortUUID().random(length=8), unique=True)
    origin = CharField()
    created_at = DateTimeField(default=datetime.now())
    redirect_count = IntegerField(default=0)
