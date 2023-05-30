from flask import Flask, request, jsonify, session
from flask import Blueprint
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity,unset_jwt_cookies, jwt_required, JWTManager
from db import DataBase
import json
import mysql.connector
from passlib.hash import sha256_crypt   

twoFactorAuthBlueprint = Blueprint('twoFactorAuthBlueprint',__name__)

dbInfo = DataBase()

# Route for register user details
@twoFactorAuthBlueprint.route('/twoFactorAuth',methods=['POST'])
def twoFactorAuth():
    # Checking for Request Method
    if request.method=='POST':
        if 'cookie' in session:
            if 'accessToken' in session:    
                session.pop("accessToken")
            data = request.get_json()
            username = data['username']
            otp = data['otp']
            try:
                dbInfo.createDatabase()
                db = mysql.connector.connect(host=dbInfo.mysql_host,user=dbInfo.mysql_user,password=dbInfo.mysql_password,database=dbInfo.database)
                db_cursor = db.cursor()

            except Exception as e:
                return {
                    "message":str(e),
                    "status":False
                }
            try:

                if ('loginOtp' in session and sha256_crypt.verify(otp,session['loginOtp'])) and ('username' in session and username==session['username']):
                    token = create_access_token(identity=username)
                    session.pop("loginOtp")
                    session.pop("loginOtpStatus")
                    return jsonify({
                        "details":{
                            "token":str(token),
                            "name":str(session['name']),
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

                
            except Exception as e:
                return {
                    "message":str(e),
                    "status":False
                }
        else:
            return jsonify({
                "message":"Access Denied",
                "type":False
            })
    else:
        return jsonify({
            "message":"Error! Invalid Method"
        })