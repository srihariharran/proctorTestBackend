from flask import Flask, request, jsonify,session
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity,unset_jwt_cookies, jwt_required, JWTManager
from flask import Blueprint
from db import DataBase
import mysql.connector
import json
from passlib.hash import sha256_crypt   

getQuestionDetailsBlueprint = Blueprint('getQuestionDetailsBlueprint',__name__)

dbInfo = DataBase()

# Route for register user details
@getQuestionDetailsBlueprint.route('/question/getDetails',methods=['POST'])
@jwt_required()
def getQuestionDetails():
    # Checking for Request Method
    if request.method=='POST':
        if 'cookie' in session:
            data=request.get_json()
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
                db_cursor.execute("SELECT * FROM "+tb_name)
                result=db_cursor.fetchall()
                responseJson=[]
                for res in result:
                    if str(res[2])=="None":
                        options="None"
                    else:
                        options=json.loads(res[2].decode('utf8'))
                    responseJson.append(
                        {
                            "courseId":courseId,
                            "questionId":res[0],
                            "question":res[1],
                            "options":options,
                            "correctAnswer":res[3],
                            "createdBy":res[4],
                            "createdOn":res[5],
                            "lastUpdated":res[6]
                        }
                    )
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