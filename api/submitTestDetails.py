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
                print(data)
                courseId=data["courseId"]
                tb_name=str(courseId)+"_test_report"
                dbInfo.createTestReportTable(tb_name)
                details=data["details"]
                webcamCount=data["webcamCount"]
                tabSwitchCount=data["tabSwitchCount"]
                submittedBy=session['username']
                submittedOn=dt.utcnow()
                submittedOn=submittedOn.isoformat("T")
                submittedOn=submittedOn[0:23] + "Z"
                db_cursor.execute("INSERT INTO "+tb_name+" (details,tabSwitchCount,webcamCount,submittedBy,submittedOn) VALUES (%s,%s,%s,%s,%s)",(json.dumps(details),tabSwitchCount,webcamCount,submittedBy,submittedOn))
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
                "message":"Access Denied",
                "status":False
            })
    else:
        return jsonify({
            "message":"Error! Invalid Method",
            "status":False
        })