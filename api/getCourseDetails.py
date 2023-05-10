from flask import Flask, request, jsonify,session
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity,unset_jwt_cookies, jwt_required, JWTManager
from flask import Blueprint
from db import DataBase
import mysql.connector
import json
from passlib.hash import sha256_crypt   

getCourseDetailsBlueprint = Blueprint('getCourseDetailsBlueprint',__name__)

dbInfo = DataBase()

# Route for register user details
@getCourseDetailsBlueprint.route('/course/getDetails',methods=['POST'])
@jwt_required()
def getCourseDetails():
    # Checking for Request Method
    if request.method=='POST':
        if 'cookie' in session:
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
                dbInfo.createCourseTable()
                db_cursor.execute("SELECT * FROM courses")
                result=db_cursor.fetchall()
                responseJson=[]
                for res in result:
                    question_tb_name=str(res[0])+"_questions"
                    tbDetail=dbInfo.checkQuestionTableExists(question_tb_name)
                    if((tbDetail['status'])):
                        db_cursor.execute("SELECT COUNT(id) FROM "+question_tb_name)
                        totalNoOfQuestion=db_cursor.fetchall()[0][0]
                    else:
                        totalNoOfQuestion=0
                    
                    if  (res[2]==1):
                        mode="private"
                    else:
                        mode="public"

                    if  (res[5]==1):
                        webcam="yes"
                    else:
                        webcam="no"
                    if str(res[10])=="None":
                        users="None"
                    else:
                        users=json.loads(res[10].decode('utf8'))
                    responseJson.append(
                        {
                            "courseId":res[0],
                            "courseName":res[1],
                            "mode":mode,
                            "duration":res[3],
                            "noOfQuestion":res[4],
                            "totalNoOfQuestion":totalNoOfQuestion,
                            "webcam":webcam,
                            "startTime":res[8],
                            "endTime":res[9],
                            "users":users,
                            "createdBy":res[11],
                            "createdOn":res[12]
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