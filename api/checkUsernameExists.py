from flask import Flask, request, jsonify,session
from flask import Blueprint
from db import DataBase
import mysql.connector
import json
from passlib.hash import sha256_crypt   

checkUsernameExistsBlueprint = Blueprint('checkUsernameExistsBlueprint',__name__)

dbInfo = DataBase()

# Route for register user details
@checkUsernameExistsBlueprint.route('/checkUsernameExists',methods=['POST'])
def checkUsernameExists():
    # Checking for Request Method
    if request.method=='POST':
        
        data=request.get_json()
        username=data['username']
        # print(username)
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
            user_result=db_cursor.fetchall()
            user_count=db_cursor.rowcount
            if user_count>0:
                return jsonify({
                    "message":"username exists",
                    "status":False
                })
            else:
                return jsonify({
                    "message":"username not exists",
                    "status":True
                })
            
        except Exception as e:
            return {
                "message":str(e),
                "status":False
            }
       
    else:
        return jsonify({
            "message":"Error! Invalid Method",
            "type":False
        })