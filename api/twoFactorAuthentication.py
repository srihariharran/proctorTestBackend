from flask import Flask, request, jsonify, session
from flask import Blueprint
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity,unset_jwt_cookies, jwt_required, JWTManager
from db import DataBase
import json
import mysql.connector
import redis
from datetime import datetime,timedelta
from passlib.hash import sha256_crypt   

twoFactorAuthBlueprint = Blueprint('twoFactorAuthBlueprint',__name__)

dbInfo = DataBase()

# Route for register user details
@twoFactorAuthBlueprint.route('/twoFactorAuth',methods=['POST'])
def twoFactorAuth():
    # Checking for Request Method
    if request.method=='POST':
        
        if 'accessToken' in session:    
            session.pop("accessToken")
        data = request.get_json()
        username = data['username']
        otp = data['otp']
        try:
            dbInfo.createDatabase()
            db = mysql.connector.connect(host=dbInfo.mysql_host,user=dbInfo.mysql_user,password=dbInfo.mysql_password,database=dbInfo.database)
            db_cursor = db.cursor()
            # redis_cli=redis.Redis(host=dbInfo.redis_host,port=dbInfo.redis_port)
            redis_cli=redis.from_url(dbInfo.redis_url)

        except Exception as e:
            return {
                "message":str(e),
                "status":False
            }
        try:
            redis_key=username
            if (redis_key and redis_cli.exists(redis_key)):
                redis_details=json.loads(redis_cli.get(redis_key).decode("utf-8"))
                if ('loginOtp' in redis_details and sha256_crypt.verify(otp,redis_details['loginOtp'])):
                    token = create_access_token(identity=username)
                    updated_redis_details={}
                    updated_redis_details.update(redis_details)
                    updated_redis_details.pop("loginOtp",None)
                    updated_redis_details.pop("loginOtpStatus",None)
                    redis_cli.setex(redis_key,timedelta(minutes=15),json.dumps(updated_redis_details))
                    return jsonify({
                        "details":{
                            "token":str(token),
                            "name":str(redis_details['name']),
                            "username":str(username),
                        },
                        "message":"User Login Successfull",
                        "status":True,
                    })
                else:
                    return jsonify({
                        "message":"Invalid OTP",
                        "status":False
                    })

            else:
                return jsonify({
                    "message":"Login Expired",
                    "status":False
                })
        except Exception as e:
            return {
                "message":str(e),
                "status":False
            }
        
    else:
        return jsonify({
            "message":"Error! Invalid Method"
        })