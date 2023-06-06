from flask import Flask, request, jsonify,session
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity,unset_jwt_cookies, jwt_required, JWTManager
from flask import Blueprint
from db import DataBase
import mysql.connector
import json
from passlib.hash import sha256_crypt   

getReportDetailsBlueprint = Blueprint('getReportDetailsBlueprint',__name__)

dbInfo = DataBase()

# Route for register user details
@getReportDetailsBlueprint.route('/report/getDetails',methods=['POST'])
@jwt_required()
def getReportDetails():
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
            dbInfo.createTestReportTable(report_tb_name)
            username=get_jwt_identity()
            reportId=data['reportId']
            db_cursor.execute("SELECT * FROM "+report_tb_name+" WHERE id=%s",(reportId,))
            result=db_cursor.fetchall()
            responseJson={}
            
            for res in result:
                details=json.loads(res[5])
                if details["webcam"]==1:
                    webcam="yes"
                else:
                    webcam="no"
                responseJson={
                        "mode":details["mode"],
                        "duration":details["duration"],
                        "noOfQuestion":details["noOfQuestion"],
                        "webcam":webcam,
                        "image":details["image"],
                        "startedOn":res[7],
                        "submittedOn":res[8],
                        "webcamCount":res[3],
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