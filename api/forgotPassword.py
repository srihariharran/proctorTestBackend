from flask import Flask, request, jsonify, session
from flask import Blueprint
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity,unset_jwt_cookies, jwt_required, JWTManager
from db import DataBase
import json
import mysql.connector
from datetime import datetime,timedelta
import redis
from passlib.hash import sha256_crypt   

forgotPasswordBlueprint = Blueprint('forgotPasswordBlueprint',__name__)

dbInfo = DataBase()

# Route for register user details
@forgotPasswordBlueprint.route('/forgotPassword',methods=['POST'])
def forgotPassword():
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

            dbInfo.createUserTable()
            db_cursor.execute("SELECT username FROM user WHERE username=%s",(username,))
            result = db_cursor.fetchall()
            row = db_cursor.rowcount
            if row==1:
                otp=dbInfo.generate_otp()
                # print(otp)
                redis_details={
                    
                    "forgotOtp":sha256_crypt.hash(otp),
                    "forgotOtpStatus":True,
                }
                redis_cli.setex(username,timedelta(minutes=15),json.dumps(redis_details))
                masked_email=username.split("@")
                message="""
                    <h3>Proctor Test</h3>
                    <h5><b>One Time Password for Forgot Password</b></h5>
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
            else:
                return jsonify({
                    "message":"Invalid Username",
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