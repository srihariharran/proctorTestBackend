from flask import Flask, request, jsonify, session
from flask import Blueprint
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity,unset_jwt_cookies, jwt_required, JWTManager
from db import DataBase
import json
import mysql.connector
import redis
from datetime import datetime,timedelta
from passlib.hash import sha256_crypt   

resetPasswordBlueprint = Blueprint('resetPasswordBlueprint',__name__)

dbInfo = DataBase()

# Route for register user details
@resetPasswordBlueprint.route('/resetPassword',methods=['POST'])
def resetPassword():
    # Checking for Request Method
    if request.method=='POST':
        
        if 'accessToken' in session:    
            session.pop("accessToken")
        data = request.get_json()
        username = data['username']
        otp=data['otp']
        password=sha256_crypt.hash(data['password'])
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

            dbInfo.createUserTable()
            redis_key=username
            if (redis_key and redis_cli.exists(redis_key)):
                redis_details=json.loads(redis_cli.get(redis_key).decode("utf-8"))
                if ('forgotOtp' in redis_details and sha256_crypt.verify(otp,redis_details['forgotOtp'])):
                    db_cursor.execute("UPDATE user SET password=%s WHERE username=%s",(password,username))
                    db.commit()
                    updated_redis_details={}
                    updated_redis_details.update(redis_details)
                    updated_redis_details.pop("forgotOtp",None)
                    updated_redis_details.pop("forgotOtpStatus",None)
                    redis_cli.setex(redis_key,timedelta(minutes=15),json.dumps(updated_redis_details))
                    return jsonify({
                        "message":"Password Reset Successfull",
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