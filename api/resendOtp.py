from flask import Flask, request, jsonify, session
from flask import Blueprint
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity,unset_jwt_cookies, jwt_required, JWTManager
from db import DataBase
import json
import mysql.connector
from passlib.hash import sha256_crypt   

resendOTPBlueprint = Blueprint('resendOTPBlueprint',__name__)

dbInfo = DataBase()

# Route for register user details
@resendOTPBlueprint.route('/resendOTP',methods=['POST'])
def resendOTP():
    # Checking for Request Method
    if request.method=='POST':
        if 'cookie' in session:
            if 'accessToken' in session:    
                session.pop("accessToken")
            data = request.get_json()
            username = data['username']
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
                db_cursor.execute("SELECT username FROM user WHERE username=%s",(username,))
                result = db_cursor.fetchall()
                row = db_cursor.rowcount
                if row==1:
                    otp=dbInfo.generate_otp()
                    print(otp)
                    if 'loginOtpStatus' in session and session['loginOtpStatus']:
                        msg_type="Login"
                        if 'forgotOtpStatus' in session:
                            session.pop('forgotOtpStatus')
                        session['loginOtpStatus']=True
                        session['loginOtp']=sha256_crypt.hash(otp)
                    else:
                        msg_type="Forgot Password"
                        if 'loginOtpStatus' in session:
                            session.pop('loginOtpStatus')
                        session['forgotOtpStatus']=True
                        session['forgotOtp']=sha256_crypt.hash(otp)
                    masked_email=username.split("@")
                    message="""
                        <h3>Proctor Test</h3>
                        <h5><b>One Time Password for """+msg_type+"""/b></h5>
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
                    # dbInfo.send_mail(message,[username],"One Time Password")
                    return jsonify({
                        "message":"OTP send to your email",
                        "status":True,
                        
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
                "message":"Access Denied",
                "type":False
            })
    else:
        return jsonify({
            "message":"Error! Invalid Method"
        })