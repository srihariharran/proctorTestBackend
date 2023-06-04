from flask import Flask, request, jsonify,session
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity,unset_jwt_cookies, jwt_required, JWTManager
from flask import Blueprint
from db import DataBase
import mysql.connector
import json
from passlib.hash import sha256_crypt   
from datetime import datetime as dt

submitTestDetailsBlueprint = Blueprint('submitTestDetailsBlueprint',__name__)

dbInfo = DataBase()

# Route for register user details
@submitTestDetailsBlueprint.route('/test/submitDetails',methods=['POST'])
@jwt_required()
def submitTestDetails():
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
            # print(data)
            courseId=data["courseId"]
            # reportId=data["reportId"]
            tb_name=str(courseId)+"_test_report"
            dbInfo.createTestReportTable(tb_name)
            details=data["details"]
            images=data["images"]
            webcamCount=data["webcamCount"]
            tabSwitchCount=data["tabSwitchCount"]
            submittedBy=get_jwt_identity()
            submittedOn=dt.utcnow()
            submittedOn=submittedOn.isoformat("T")
            submittedOn=submittedOn[0:23] + "Z"
            ip=data['ip']
            platform=data['platform']
            # print(data)
            if 'reportId' in data and data['reportId']!='':
                reportId=data['reportId']
            else:
                query="SELECT id FROM "+tb_name+" WHERE testDetails LIKE '%"+str(ip)+"%' AND testDetails LIKE '%"+str(platform)+"%' ORDER BY id DESC LIMIT 1"
                db_cursor.execute(query)
                reportId=db_cursor.fetchall()[0][0]
            # print(reportId)
            db_cursor.execute("UPDATE "+tb_name+" SET questionDetails=%s,tabSwitchCount=%s,webcamCount=%s,doubtImages=%s,submittedOn=%s WHERE id=%s",(json.dumps(details),tabSwitchCount,webcamCount,json.dumps(images),submittedOn,reportId))
            db.commit()
            return jsonify({
                "message":"Test Submitted Successfully",
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