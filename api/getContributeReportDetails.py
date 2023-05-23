from flask import Flask, request, jsonify,session
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity,unset_jwt_cookies, jwt_required, JWTManager
from flask import Blueprint
from db import DataBase
import mysql.connector
import json
from passlib.hash import sha256_crypt   

getContributeReportDetailsBlueprint = Blueprint('getContributeReportDetailsBlueprint',__name__)

dbInfo = DataBase()

# Route for register user details
@getContributeReportDetailsBlueprint.route('/contribute/report/getDetails',methods=['POST'])
@jwt_required()
def getContributeReportDetails():
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
                tb_name=str(courseId)+"_test_report"
                dbInfo.createQuestionTable(tb_name)
                username=session['username']
                
                db_cursor.execute("SELECT * FROM "+tb_name+" LEFT JOIN user ON "+tb_name+".submittedBy=user.username WHERE "+tb_name+".startedOn IS NOT NULL AND "+tb_name+".submittedOn IS NOT NULL  ORDER BY "+tb_name+".id DESC")
                result=db_cursor.fetchall()
                responseJson=[]
                print(result)
                question_tb_name=str(courseId)+"_questions"
                for res in result:
                    score=0
                    details=json.loads(res[5].decode('utf8'))
                    questionDetails=json.loads(res[1].decode('utf8'))
                    for questionRes in questionDetails:
                        question=questionDetails[questionRes]["question"]
                        answer=questionDetails[questionRes]["answer"]
                        db_cursor.execute("SELECT options,correctAnswer FROM "+question_tb_name+" WHERE question=%s",(question,))
                        optionResult=db_cursor.fetchall()
                        for optionRes in optionResult:
                            if str(answer)==str(optionRes[1]):
                                score=score+1
                    if details["webcam"]==1:
                        webcam="yes"
                    else:
                        webcam="no"
                    responseJson.append(
                        {
                            "mode":details["mode"],
                            "duration":details["duration"],
                            "noOfQuestion":details["noOfQuestion"],
                            "webcam":webcam,
                            "reportId":res[0],
                            "startedOn":res[7],
                            "submittedOn":res[8],
                            "score":score,
                            "name":res[11],
                            "email":res[9]
                        }
                    )
                return jsonify(responseJson)
            except Exception as e:
                # print(e)  
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