from flask import Flask, request, jsonify, session
from flask import Blueprint
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity,unset_jwt_cookies, jwt_required, JWTManager
from db import DataBase
import json
import mysql.connector
from datetime import datetime,timedelta
import redis
from passlib.hash import sha256_crypt   

logoutBlueprint = Blueprint('logoutBlueprint',__name__)

dbInfo = DataBase()

# Route for register user details
@logoutBlueprint.route('/logout',methods=['POST'])
@jwt_required()
def logout():
    # Checking for Request Method
    if request.method=='POST':
        redis_key=get_jwt_identity()
        jti = get_jwt()["jti"]
        # session["accessToken"]=jti
        # redis_cli=redis.Redis(host=dbInfo.redis_host,port=dbInfo.redis_port)
        redis_cli=redis.from_url(dbInfo.redis_url)
        redis_details=redis_cli.get("logoutUsers")
        redis_cli.delete(redis_key)
        redis_cli.setex("logoutUsers",timedelta(minutes=15),jti)
        return jsonify({
            "message":"Logout Successfull",
            "status":True
        })
       
    else:
        return jsonify({
            "message":"Error! Invalid Method"
        })