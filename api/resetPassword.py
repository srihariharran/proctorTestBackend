from flask import Flask, request, jsonify, session
from flask import Blueprint
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity,unset_jwt_cookies, jwt_required, JWTManager
from db import DataBase
import json
import mysql.connector
from passlib.hash import sha256_crypt   

resetPasswordBlueprint = Blueprint('resetPasswordBlueprint',__name__)

dbInfo = DataBase()

# Route for register user details
@resetPasswordBlueprint.route('/resetPassword',methods=['POST'])
def resetPassword():
    # Checking for Request Method
    if request.method=='POST':
        if 'cookie' in session:
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

            except Exception as e:
                return {
                    "message":str(e),
                    "status":False
                }
            try:

                dbInfo.createUserTable()
                if ('forgotOtp' in session and sha256_crypt.verify(otp,session['forgotOtp'])) and ('username' in session and username==session['username']):
                    db_cursor.execute("UPDATE user SET password=%s WHERE username=%s",(password,username))
                    db.commit()
                    session.pop("forgotOtp")
                    session.pop("forgotOtpStatus")
                    return jsonify({
                        "message":"Password Reset Successfull",
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