from flask import Flask, request, jsonify,session
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity,unset_jwt_cookies, jwt_required, JWTManager
from flask import Blueprint
from db import DataBase
import mysql.connector
import json
from passlib.hash import sha256_crypt   
from datetime import datetime as dt

deleteQuestionDetailsBlueprint = Blueprint('deleteQuestionDetailsBlueprint',__name__)

dbInfo = DataBase()

# Route for register user details
@deleteQuestionDetailsBlueprint.route('/question/deleteDetails',methods=['POST'])
@jwt_required()
def deleteQuestionDetails():
    # Checking for Request Method
    if request.method=='POST':
        
        data = request.get_json()
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
            courseId=data["courseId"]
            tb_name=str(courseId)+"_questions"
            dbInfo.createQuestionTable(tb_name)
            questionId=data["questionId"]
            db_cursor.execute("DELETE FROM "+tb_name+" WHERE id=%s",(questionId,))
            db.commit()
            
            return jsonify({
                "message":"Question Removed Successfully",
                "status":True
            })
            return jsonify(responseJson)
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