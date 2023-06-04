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
                duration=res[3]
                noOfQuestion=res[4]
                question_tb_name=str(res[0])+"_questions"
                tbDetail=dbInfo.checkQuestionTableExists(question_tb_name)
                if((tbDetail['status'])):
                    db_cursor.execute("SELECT COUNT(id) FROM "+question_tb_name)
                    totalNoOfQuestion=db_cursor.fetchall()[0][0]
                else:
                    totalNoOfQuestion=0
                
                report_tb_name=str(res[0])+"_test_report"
                dbInfo.createTestReportTable(report_tb_name)
                username=get_jwt_identity()
                # print(username)
                db_cursor.execute("SELECT count(id) FROM "+report_tb_name+" group by submittedBy")
                report_count_data=db_cursor.fetchall()
                report_count=0
                for report_c_res in report_count_data:
                    report_count=report_c_res
                db_cursor.execute("SELECT id,startedOn,submittedOn,testDetails FROM "+report_tb_name+" WHERE submittedBy=%s  ORDER BY id DESC LIMIT 1",(username,))
                report_result=db_cursor.fetchall()
                
                if(db_cursor.rowcount==0):
                    reportId,startedOn,submittedOn='','',''
                else:
                    for r_res in report_result:
                        reportId=r_res[0]
                        startedOn=r_res[1]
                        submittedOn=r_res[2]
                        
                        if startedOn!=None and submittedOn==None:
                            details=json.loads(r_res[3])
                            duration=details["duration"]
                            noOfQuestion=details["noOfQuestion"]
                        

                
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
                    users=json.loads(res[10])
                
                responseJson.append(
                    {
                        "courseId":res[0],
                        "courseName":res[1],
                        "mode":mode,
                        "duration":duration,
                        "noOfQuestion":noOfQuestion,
                        "totalNoOfQuestion":totalNoOfQuestion,
                        "webcam":webcam,
                        "startTime":res[8],
                        "endTime":res[9],
                        "users":users,
                        "tabSwitch":res[7],
                        "webcamLimit":res[6],
                        "createdBy":res[11],
                        "createdOn":res[12],
                        "reportId":reportId,
                        "startedOn":startedOn,
                        "submittedOn":submittedOn,
                        "testTaken":report_count
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
            "message":"Error! Invalid Method",
            "status":False
        })