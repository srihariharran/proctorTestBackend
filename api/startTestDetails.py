from flask import Flask, request, jsonify,session
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity,unset_jwt_cookies, jwt_required, JWTManager
from flask import Blueprint
from db import DataBase
import mysql.connector
import json
from passlib.hash import sha256_crypt   
from datetime import datetime as dt

startTestDetailsBlueprint = Blueprint('startTestDetailsBlueprint',__name__)

dbInfo = DataBase()

# Route for register user details
@startTestDetailsBlueprint.route('/test/startDetails',methods=['POST'])
@jwt_required()
def startTestDetails():
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
                courseId=data["courseId"]
                tb_name=str(courseId)+"_test_report"
                dbInfo.createTestReportTable(tb_name)
                webcam=data['webcam']
                testDetails={
                    "mode":data["mode"],
                    "duration":data["duration"],
                    "noOfQuestion":data["noOfQuestion"],
                    "ip":data["ip"],
                    "platform":data["platform"]
                }
                if webcam=="yes":
                    testDetails.update({
                        "webcam":1,
                        "image":data["image"]
                    })
                else:
                    testDetails.update({
                        "webcam":0,
                        "image":''
                    })

                submittedBy=session['username']
                startedOn=dt.utcnow()
                startedOn=startedOn.isoformat("T")
                startedOn=startedOn[0:23] + "Z"
                db_cursor.execute("INSERT INTO "+tb_name+" (testDetails,submittedBy,startedOn) VALUES (%s,%s,%s)",(json.dumps(testDetails),submittedBy,startedOn))
                db.commit()
                db_cursor.execute("SELECT id FROM "+tb_name+" WHERE submittedBy=%s AND startedOn=%s",(submittedBy,startedOn))
                id_result=db_cursor.fetchall()[0][0]
                return jsonify({
                    "id":str(id_result),
                    "message":"Test Started Successfully",
                    "status":True
                })
                return jsonify(responseJson)
            except Exception as e:
                print(e)
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