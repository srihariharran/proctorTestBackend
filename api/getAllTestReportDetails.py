from flask import Flask, request, jsonify,session
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity,unset_jwt_cookies, jwt_required, JWTManager
from flask import Blueprint
from db import DataBase
import mysql.connector
import json
from passlib.hash import sha256_crypt   

getAllTestReportDetailsBlueprint = Blueprint('getAllTestReportDetailsBlueprint',__name__)

dbInfo = DataBase()

# Route for register user details
@getAllTestReportDetailsBlueprint.route('/test/report/all/getDetails',methods=['POST'])
@jwt_required()
def getAllTestReportDetails():
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
                db_cursor.execute("SELECT * FROM "+tb_name+" WHERE submittedBy=%s AND startedOn IS NOT NULL AND submittedOn IS NOT NULL  ORDER BY id DESC",(username,))
                result=db_cursor.fetchall()
                responseJson=[]
                for res in result:
                    details=json.loads(res[5].decode('utf8'))
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
                            "submittedOn":res[8]
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