import models
import os
import sys
import secrets
from PIL import Image
from flask import Blueprint, request, jsonify, url_for, send_file
from playhouse.shortcuts import model_to_dict

api = Blueprint('api', 'api2', url_prefix="/api/v1")
# added api2 to second arg in above line bc was getting errors from 'api'

def color_value(form_picture):
   output_size = (10, 10)
   i = Image.open(form_picture)
   i.thumbnail(output_size)
   dims = i.size
   print(i.size, '<--- image size')
   pix = i.load()
   color_str = ''
   for x in range (0,i.size[0]):
       for y in range (0,i.size[1]):
           rgb_values = pix[x,y]
           count = (x,y)
           key_val = str(count) + '\t' + str(rgb_values)
           print(key_val)
           color_str = color_str + key_val + '\n'
           #color_dict.join(key_val)
   print(color_str)
   return color_str 
@api.route('/bins/', methods=["POST"])
def create_bin():
    print(request, '<--request')
    payload = request.form.to_dict()
    print(payload, '<-payload', type(payload), 'type')
    item = models.Bin.create(size=payload['size'],userId=payload['userId'])
    item_dict = model_to_dict(item)
    print(item.__dict__)
    return jsonify(data=item_dict, status={"code":201, "message":"success"})

@api.route('/items/', methods=["POST"])
def create_junk():
    print(request, '<--request')
    print(request.files, '<--request.files')
    pay_file = request.files
    payload = request.form.to_dict()
    dict_file = pay_file.to_dict()
    print(payload, '<-- payload')
    print(dict_file, '<--dict_file')
    color = color_value(dict_file['file'])
    payload['color'] = color 
    print(payload, '<-payload')
    item = models.Item.create(**payload)
    item_dict = model_to_dict(item)
    print(item.__dict__)
    return jsonify(data=item_dict, status={"code":201, "message":"success"})

@api.route('/items/', methods=["GET"])
def get_all_items():
    try: 
        items = [model_to_dict(item) for item in models.Item.select()]
        return jsonify(data=items, status={"code": 200, "message":"success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "seems to be a problem retrieving"})

@api.route('/<id>', methods=["DELETE"])
def delete_shrub(id):
    query = models.Item.delete().where(models.Item.id == id)
    query.execute()
    return jsonify(data="delete successful", status={"code": 200, "message":"resource succesfully deleted"})

@api.route('/bins/', methods=["GET"])
def get_all_bins():
    try:
        bins = [model_to_dict(binn) for binn in models.Bin.select()]
        print(bins)
        return jsonify(data=bins, status={"code": 200, "message":"success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "oh no"})
