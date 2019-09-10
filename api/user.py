import models
import os
import sys
import secrets
from PIL import Image
from flask_login import login_user, current_user
from flask import Blueprint, request, jsonify, url_for, send_file
from playhouse.shortcuts import model_to_dict

user = Blueprint('users', 'user', url_prefix='/user')

@user.route('/register', methods=["POST"])
def register():
    print(request)
    payload = request.get_json()
    print(payload)
    try:
        models.User.get(models.User.uid == payload['uid'])
        return jsonify(data={}, status={"code": 401, "message": "a user w that uid already exists"})
    except models.DoesNotExist:
        user = models.User.create(**payload)
        login_user(user)
        user_dict = model_to_dict(user)
        print(user_dict, '<----- user dict')
        return jsonify(data=user_dict, status={"code": 201, "message": "Success"})

@user.route('/logIn', methods=["POST"])
def get_user():
    payload = request.get_json()
    print(payload)
    try: 
        user = [model_to_dict(user) for user in models.User.select().where(models.User.uid == payload)]
        return jsonify(data=user, status={"code": 200, "message":"success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "seems to be a problem retrieving"})

@user.route('/<id>/profile', methods=["GET"])
def get_bins_from_user(id):
   user = models.User.get_by_id(id)
   user.get()
   try:
       bins = [model_to_dict(bin) for bin in models.Bin.select().where(models.Bin.userId == id)]
       print(bins, '<--- bins')
       return jsonify(data=bins, status={"code":200,"message":"success"})
   except models.DoesNotExists:
      return jsonify(data={}, status={"code": 401, "message": "there was an error adding the resource"})

