from flask import Flask, request, jsonify, session
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity,unset_jwt_cookies, jwt_required, JWTManager
from flask import Blueprint
from db import DataBase
import json
import mysql.connector
from passlib.hash import sha256_crypt  
from datetime import datetime 
import redis

updateUserBlueprint = Blueprint('updateUserBlueprint',__name__)

dbInfo = DataBase()

# Route for update user details
@updateUserBlueprint.route('/update/user',methods=['POST'])
@jwt_required()
def updateUser():
    # Checking for Request Method
    if request.method=='POST':
        
        data=request.get_json()
        username=data['username']
        
        name=data['name']
        organisation=data['organisation']
        designation=data['designation']
        mobile=data['mobile']
        twoFactorAuth=data['twoFactorAuth']
        updatedOn=datetime.utcnow()
        updatedOn=updatedOn.isoformat("T")
        updatedOn=updatedOn[0:23] + "Z"
        if twoFactorAuth:
            twoFactorAuth=1
        else:
            twoFactorAuth=0
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
            if data["password"]=="password" or data["password"]=='':
                db_cursor.execute("UPDATE user SET name=%s,organisation=%s,designation=%s,mobile=%s,twoFactorAuth=%s,lastUpdated=%s WHERE username=%s",(name,organisation,designation,mobile,twoFactorAuth,updatedOn,username))
                db.commit()
            else:
                password=sha256_crypt.hash(data['password'])
                db_cursor.execute("UPDATE user SET name=%s,organisation=%s,designation=%s,mobile=%s,password=%s,twoFactorAuth=%s,lastUpdated=%s WHERE username=%s",(name,organisation,designation,mobile,password,twoFactorAuth,updatedOn,username))
                db.commit()
            return jsonify({
                "message":"Profile Updated Successfully",
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