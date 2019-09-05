import models
import os
import sys
import secrets
from PIL import Image

from flask import Blueprint, request, jsonify, url_for, send_file
from playhouse.shortcuts import model_to_dict
api = Blueprint('api', 'api2', url_prefix="/api/v1")
# added api2 to second arg in above line bc was getting errors from 'api'

def save_picture(form_picture):
   random_hex = secrets.token_hex(8)
   f_name, f_ext = os.path.splitext(form_picture.filename)
   picture_name = random_hex + f_ext
   file_path_for_avatar = os.path.join(os.getcwd(), 'static/items' + picture_name)
   output_size = (800, 800)
   i = Image.open(form_picture)
   i.thumbnail(output_size)
   dims = i.size
   print(i.size, '<--- image size')
   width = dims[0]
   height = dims[1]
   print(width,'width',height,'height')
   i.save(file_path_for_avatar)
   return picture_name

@api.route('/', methods=["POST"])
def create_junk():
    print(request)
    pay_file = request.files
    payload = request.form.to_dict()
    dict_file = pay_file.to_dict()
    print(payload, '<-- payload')
    print(dict_file, '<--dict_file')
    file_picture_path = save_picture(dict_file['file'])
    payload['image'] = file_picture_path
    print(payload, '<-payload', type(payload), 'type')
    item = models.Junk.create(**payload)
    item_dict = model_to_dict(item)
    print(item.__dict__)
    return jsonify(data=item_dict, status={"code":201, "message":"success"})

@api.route('/', methods=["GET"])
def get_all_items():
    try: 
        items = [model_to_dict(item) for item in models.Junk.select()]
        return jsonify(data=items, status={"code": 200, "message":"success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "seems to be a problem retrieving"})
