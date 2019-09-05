from peewee import *
from flask_login import UserMixin
from flask import request
from playhouse.db_url import connect 

import datetime
import os

#DATABASE = connect(os.environ.get('DATABASE_URL'))
DATABASE = SqliteDatabase('junk2.sqlite')

#tags = db.Table('tags',
 #   db.Column('location_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
  #  db.Column('junk_id', db.Integer, db.ForeignKey('page.id'), primary_key=True)
#)
class User(UserMixin, Model):
   username = CharField()
   email = CharField()
   password = CharField()
   class Meta:
       database = DATABASE 

class Junk(Model):
    #average_red = IntegerField()
    #average_green = IntegerField()
    #average_blue = IntegerField()
    image = CharField()
    description = TextField()
    #author = ForeignKeyField(User, backref='junk')
    price = FloatField()
    class Meta:
       database = DATABASE 

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Junk], safe=True)
    print("your TABLES CREATED")
    DATABASE.close()
