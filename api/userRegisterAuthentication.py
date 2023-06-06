from flask import Flask, request, jsonify, session
from flask import Blueprint
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity,unset_jwt_cookies, jwt_required, JWTManager
from db import DataBase
import json
import mysql.connector
import redis
from datetime import datetime,timedelta
from passlib.hash import sha256_crypt   

userRegisterAuthBlueprint = Blueprint('userRegisterAuthBlueprint',__name__)

dbInfo = DataBase()

# Route for register user details
@userRegisterAuthBlueprint.route('/userRegisterAuth',methods=['POST'])
def userRegisterAuth():
    # Checking for Request Method
    if request.method=='POST':
        
        if 'accessToken' in session:    
            session.pop("accessToken")
        data = request.get_json()
        username = data['username']
        
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
            otp=dbInfo.generate_otp()
            # print(otp)
            redis_details={
                
                "registerOtp":sha256_crypt.hash(otp),
                "registerOtpStatus":True,
            }
            redis_details.update(data)
            redis_cli.setex(username,timedelta(minutes=15),json.dumps(redis_details))
            masked_email=username.split("@")
            message="""
                <h3>Proctor Test</h3>
                <h5><b>One Time Password for User Registration</b></h5>
                <br/>
                Please use the following OTP for the proctor test account
                <br/>
                <br/>
                One Time Password: <b>"""+otp+"""</b>
                <br/>
                <br/>
                Thanks,
                <br/>
                Proctor Test
            """
            dbInfo.send_mail(message,[username],"One Time Password")
            return jsonify({
                "message":"OTP send to your email",
                "status":True,
                "otpMaskedEmail":masked_email[0][:2]+'*'*(len(masked_email[0])-3)+masked_email[0][-2:]+'@'+masked_email[1]
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