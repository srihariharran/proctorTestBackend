from flask import Flask, request, jsonify, session
from flask import Blueprint
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity,unset_jwt_cookies, jwt_required, JWTManager
from db import DataBase
import json
import mysql.connector
import redis
from passlib.hash import sha256_crypt   
from datetime import datetime,timedelta

loginBlueprint = Blueprint('loginBlueprint',__name__)

dbInfo = DataBase()

# Route for register user details
@loginBlueprint.route('/login',methods=['POST'])
def login():
    # Checking for Request Method
    if request.method=='POST':
        
        if 'accessToken' in session:    
            session.pop("accessToken")
        data = request.get_json()
        username = data['username']
        password = data['password']
        try:
            dbInfo.createDatabase()
            db = mysql.connector.connect(host=dbInfo.mysql_host,user=dbInfo.mysql_user,password=dbInfo.mysql_password,database=dbInfo.database)
            db_cursor = db.cursor()
            try:
                # redis_cli=redis.Redis(host=dbInfo.redis_host,port=dbInfo.redis_port,password=dbInfo.redis_password)
                redis_cli=redis.from_url(dbInfo.redis_url)
            except Exception as e:
                print(str(e)+" abdahkbdik")


        except Exception as e:
            return {
                "message":str(e),
                "status":False
            }
        try:
            dbInfo.createUserTable()
            db_cursor.execute("SELECT * FROM user WHERE username=%s",(username,))
            result = db_cursor.fetchall()
            row = db_cursor.rowcount
            if row==1:
                for res in result:
                    if sha256_crypt.verify(password,res[1]):
                        
                        if res[8]==1:
                            otp=dbInfo.generate_otp()
                            
                            
                            
                            masked_email=res[0].split("@")
                            message="""
                                <h3>Proctor Test</h3>
                                <h5><b>One Time Password for Login</b></h5>
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
                            redis_details={
                                "name":res[2],
                                "loginOtp":sha256_crypt.hash(otp),
                                "loginOtpStatus":True,
                            }
                            redis_cli.setex(username,timedelta(minutes=15),json.dumps(redis_details))
                            return jsonify({
                                "message":"OTP send to your email",
                                "status":True,
                                "otpStatus":True,
                                "otpMaskedEmail":masked_email[0][:2]+'*'*(len(masked_email[0])-3)+masked_email[0][-2:]+'@'+masked_email[1]
                            })
                        else:
                            token = create_access_token(identity=username)
                            redis_details={
                                "name":res[2]
                            }
                            redis_cli.setex(username,timedelta(minutes=15),json.dumps(redis_details))
                            return jsonify({
                                "details":{
                                    "token":str(token),
                                    "name":str(res[2]),
                                    "username":str(res[0]),
                                },
                                "message":"User Login Successfull",
                                "status":True,
                                "otpStatus":False
                            })
                    else:
                        return jsonify({
                            "message":"Invalid Password",
                            "status":False
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