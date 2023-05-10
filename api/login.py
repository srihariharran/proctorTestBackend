from flask import Flask, request, jsonify, session
from flask import Blueprint
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity,unset_jwt_cookies, jwt_required, JWTManager
from db import DataBase
import json
import mysql.connector
from passlib.hash import sha256_crypt   

loginBlueprint = Blueprint('loginBlueprint',__name__)

dbInfo = DataBase()

# Route for register user details
@loginBlueprint.route('/login',methods=['POST'])
def login():
    # Checking for Request Method
    if request.method=='POST':
        if 'cookie' in session:
            if 'accessToken' in session:    
                session.pop("accessToken")
            data = request.get_json()
            username = data['username']
            password = data['password']
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
                db_cursor.execute("SELECT * FROM user WHERE username=%s",(username,))
                result = db_cursor.fetchall()
                row = db_cursor.rowcount
                if row==1:
                    for res in result:
                        if sha256_crypt.verify(password,res[1]):
                            session["name"]=res[2]
                            session["username"]=res[0]
                            token = create_access_token(identity=username)
                            return jsonify({
                                "details":{
                                    "token":str(token),
                                    "name":str(res[2]),
                                    "username":str(res[0]),
                                },
                                "message":"User Login Successfull",
                                "status":True
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
                "message":"Access Denied",
                "type":False
            })
    else:
        return jsonify({
            "message":"Error! Invalid Method"
        })