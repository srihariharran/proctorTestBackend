from flask import Flask, request, jsonify,session
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity,unset_jwt_cookies, jwt_required, JWTManager
from flask import Blueprint
from db import DataBase
import mysql.connector
import json
from passlib.hash import sha256_crypt   

getTestReportDetailsBlueprint = Blueprint('getTestReportDetailsBlueprint',__name__)

dbInfo = DataBase()

# Route for register user details
@getTestReportDetailsBlueprint.route('/test/report/getDetails',methods=['POST'])
@jwt_required()
def getTestReportDetails():
    # Checking for Request Method
    if request.method=='POST':
       
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
            report_tb_name=str(courseId)+"_test_report"
            question_tb_name=str(courseId)+"_questions"
            dbInfo.createQuestionTable(question_tb_name)
            dbInfo.createTestReportTable(report_tb_name)
            username=get_jwt_identity()
            reportId=data['reportId']
            db_cursor.execute("SELECT * FROM "+report_tb_name+" WHERE id=%s",(reportId,))
            result=db_cursor.fetchall()
            responseJson={}
            questionJson=[]
            score=0
            for res in result:
                
                questionDetails=json.loads(res[1])
                for questionRes in questionDetails:
                    
                    question=questionDetails[questionRes]["question"]
                    answer=questionDetails[questionRes]["answer"]
                    
                    db_cursor.execute("SELECT options,correctAnswer FROM "+question_tb_name+" WHERE question=%s",(question,))
                    optionResult=db_cursor.fetchall()
                    
                    for optionRes in optionResult:
                        
                        if str(answer)==str(optionRes[1]):
                            score=score+1
                        questionJson.append(
                            {
                                "question":question,
                                "options":json.loads(optionRes[0]),
                                "answer":answer,
                                "correctAnswer":optionRes[1]
                            }
                        )
                
                details=json.loads(res[5])
                
                if details["webcam"]==1:
                    webcam="yes"
                else:
                    webcam="no"
                print(json.loads(res[4]))
                responseJson={
                        "mode":details["mode"],
                        "duration":details["duration"],
                        "noOfQuestion":details["noOfQuestion"],
                        "webcam":webcam,
                        "image":details["image"],
                        "startedOn":res[7],
                        "submittedOn":res[8],
                        "questionDetails":questionJson,
                        "tabSwitchCount":res[2],
                        "webcamCount":res[3],
                        "doubtImages":json.loads(res[4]),
                        "score":score,
                        "ip":details["ip"],
                        "platform":details["platform"]
                    }
                
            return jsonify(responseJson)
        except Exception as e:
            print(e)  
            return {
                "message":str(e),
                "status":False
            }
        
    else:
        return jsonify({
            "message":"Error! Invalid Method",
            "status":False
        })




        