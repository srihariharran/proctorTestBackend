from flask import Flask, request, jsonify, session
from flask import Blueprint
from db import DataBase
import json
import mysql.connector
import redis
from datetime import datetime,timedelta
from passlib.hash import sha256_crypt   

registerUserBlueprint = Blueprint('registerUserBlueprint',__name__)

dbInfo = DataBase()

# Route for register user details
@registerUserBlueprint.route('/register/user',methods=['POST'])
def registerUser():
    # Checking for Request Method
    if request.method=='POST':
        
        data=request.get_json()
        username=data['username']
        otp=data['otp']
        try:
            dbInfo.createDatabase()
            db = mysql.connector.connect(host=dbInfo.mysql_host,user=dbInfo.mysql_user,password=dbInfo.mysql_password,database=dbInfo.database)
            db_cursor = db.cursor()
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
                if ('registerOtp' in redis_details and sha256_crypt.verify(otp,redis_details['registerOtp'])):
                    password=sha256_crypt.hash(redis_details['password'])
                    name=redis_details['name']
                    organisation=redis_details['organisation']
                    designation=redis_details['designation']
                    mobile=redis_details['mobile']
                    createdOn=datetime.utcnow()
                    createdOn=createdOn.isoformat("T")
                    createdOn=createdOn[0:23] + "Z"
                    redis_cli.delete(redis_key)
                    dbInfo.createUserTable()
                    db_cursor.execute("INSERT INTO user (username,password,name,organisation,designation,mobile,createdOn) VALUES (%s,%s,%s,%s,%s,%s,%s)",(username,password,name,organisation,designation,mobile,createdOn))
                    db.commit()
                    return jsonify({
                        "message":"User Registered Successfully",
                        "status":True
                    })
                else:
                    return jsonify({
                        "message":"Invalid OTP",
                        "status":False
                    })
            
        except Exception as e:
            return {
                "message":str(e),
                "status":False
            }
        
    else:
        return jsonify({
            "message":"Error! Invalid Method",
            "status":False
        })