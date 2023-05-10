from flask import Flask, request, jsonify,session
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity,unset_jwt_cookies, jwt_required, JWTManager
from flask import Blueprint
from db import DataBase
import mysql.connector
import json
from passlib.hash import sha256_crypt   
from datetime import datetime as dt

editQuestionDetailsBlueprint = Blueprint('editQuestionDetailsBlueprint',__name__)

dbInfo = DataBase()

# Route for register user details
@editQuestionDetailsBlueprint.route('/question/editDetails',methods=['POST'])
@jwt_required()
def editQuestionDetails():
    # Checking for Request Method
    if request.method=='POST':
        if 'cookie' in session:
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
                question=data["question"]
                correctAnswer=data["correctAnswer"]
                lastUpdated=dt.utcnow()
                lastUpdated=lastUpdated.isoformat("T")
                lastUpdated=lastUpdated[0:23] + "Z"
                options=[]
                for res in data:
                    if "option" in res:
                        options.append(data[res])
                db_cursor.execute("UPDATE "+tb_name+" SET options=%s,correctAnswer=%s,lastUpdated=%s WHERE id=%s",(json.dumps(options),correctAnswer,lastUpdated,questionId))
                db.commit()
               
                return jsonify({
                    "message":"Question Modified Successfully",
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
                "message":"Access Denied",
                "status":False
            })
    else:
        return jsonify({
            "message":"Error! Invalid Method",
            "status":False
        })