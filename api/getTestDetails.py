from flask import Flask, request, jsonify,session
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity,unset_jwt_cookies, jwt_required, JWTManager
from flask import Blueprint
from db import DataBase
import mysql.connector
import json
from passlib.hash import sha256_crypt   

getTestDetailsBlueprint = Blueprint('getTestDetailsBlueprint',__name__)

dbInfo = DataBase()

# Route for register user details
@getTestDetailsBlueprint.route('/test/getDetails',methods=['POST'])
@jwt_required()
def getTestDetails():
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
                data=request.get_json()
                courseId=data["courseId"]
                tb_name=str(courseId)+"_questions"
                courseName=data["courseName"]
                dbInfo.createCourseTable()
                db_cursor.execute("SELECT * FROM courses WHERE id=%s",(courseId,))
                result=db_cursor.fetchall()[0]
                duration=result[3]
                if result[5]==0:
                    webcam="no"
                else:
                    webcam="yes"
                noOfQuestion=result[4]
                webcamLimit=result[6]
                tabSwitchLimit=result[7]

                if data["mode"]=="public":
                    duration=data["duration"]
                    webcam=data["webcam"]
                    noOfQuestion=data["noOfQuestion"]
                    
                dbInfo.createQuestionTable(tb_name)
                db_cursor.execute("SELECT * FROM "+tb_name+" AS t1 JOIN (SELECT id FROM "+tb_name+" ORDER BY RAND() LIMIT "+str(noOfQuestion)+") as t2 ON t1.id=t2.id")
                result=db_cursor.fetchall()
                rows=db_cursor.rowcount
                details=[]
                for res in result:
                    if str(res[2])=="None":
                        options="None"
                    else:
                        options=json.loads(res[2].decode('utf8'))
                    details.append(
                        {
                            "questionId":res[0],
                            "question":res[1],
                            "options":options,
                        }
                    )
                

                responseJson={
                    "courseId":courseId,
                    "courseName":courseName,
                    "duration":duration,
                    "tabSwitchLimit":tabSwitchLimit,
                    "webcam":webcam,
                    "noOfQuestion":rows,
                    "webcamLimit":webcamLimit,  
                    "details":details
                }
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