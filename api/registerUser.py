from flask import Flask, request, jsonify, session
from flask import Blueprint
from db import DataBase
import json
import mysql.connector
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
        password=sha256_crypt.hash(data['password'])
        name=data['name']
        organisation=data['organisation']
        designation=data['designation']
        mobile=data['mobile']
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
            db_cursor.execute("INSERT INTO user (username,password,name,organisation,designation,mobile) VALUES (%s,%s,%s,%s,%s,%s)",(username,password,name,organisation,designation,mobile))
            db.commit()
            return jsonify({
                "message":"User Registered Successfully",
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
            "status":False
        })