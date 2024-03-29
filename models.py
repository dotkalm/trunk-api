from peewee import *
from flask_login import UserMixin
from flask import request
from playhouse.db_url import connect 

import datetime
import os

DATABASE = PostgresqlDatabase('junk')
#DATABASE = connect(os.environ.get('DATABASE_URL'))
#DATABASE = SqliteDatabase('trunksale8.sqlite')

class User(UserMixin, Model):
   username = CharField()
   id = IntegerField(primary_key=True)
   uid = CharField()
   class Meta:
       database = DATABASE 

class Box(Model):
    name = CharField()

class Bin(Model):
    size = CharField()
    userId = ForeignKeyField(User, backref='user')
    class Meta:
        database = DATABASE

class Item(Model):
    fileName1 = CharField()
    fileName2 = CharField()
    color = TextField()
    avgR = IntegerField()
    avgG = IntegerField()
    avgB = IntegerField()
    image = CharField()
    thumb = CharField()
    description = TextField()
    bin = ForeignKeyField(Bin, backref='item')
    price = FloatField()
    class Meta:
       database = DATABASE 

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Item, Bin], safe=True)
    print("your TABLES CREATED")
    DATABASE.close()
