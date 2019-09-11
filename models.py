from peewee import *
from flask_login import UserMixin
from flask import request
from playhouse.db_url import connect 

import datetime
import os

DATABASE = connect(os.environ.get('DATABASE_URL'))
#DATABASE = SqliteDatabase('trunksale1.sqlite')

#tags = db.Table('tags',
 #   db.Column('location_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
  #  db.Column('junk_id', db.Integer, db.ForeignKey('page.id'), primary_key=True)
#)
class User(UserMixin, Model):
   username = CharField()
   id = IntegerField(primary_key=True)
   uid = CharField()
   class Meta:
       database = DATABASE 

class Bin(Model):
    size = CharField()
    userId = ForeignKeyField(User, backref='user')
    class Meta:
        database = DATABASE

class Item(Model):
    average_red = IntegerField()
    average_green = IntegerField()
    average_blue = IntegerField()
    image = CharField()
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
