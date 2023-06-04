from flask import Flask, request, jsonify,session
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity,unset_jwt_cookies, jwt_required, JWTManager
from flask import Blueprint
from db import DataBase
import mysql.connector
import json
from passlib.hash import sha256_crypt   

getUserDetailsBlueprint = Blueprint('getUserDetailsBlueprint',__name__)

dbInfo = DataBase()

# Route for register user details
@getUserDetailsBlueprint.route('/user/getDetails',methods=['POST'])
@jwt_required()
def getUserDetails():
    # Checking for Request Method
    if request.method=='POST':
        
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
            username=get_jwt_identity()
            db_cursor.execute("SELECT * FROM user WHERE username!=%s",(username,))
            result=db_cursor.fetchall()
            responseJson=[]
            for res in result:
                responseJson.append(
                    {
                        "username":res[0],
                        "name":res[2],
                        
                    }
                )
            # print(responseJson)
            return jsonify(responseJson)
        except Exception as e:
            # print(e)
            return {
                "message":str(e),
                "status":False
            }
        
    else:
        return jsonify({
            "message":"Error! Invalid Method",
            "status":False
        })