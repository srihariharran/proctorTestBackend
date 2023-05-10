from flask import Flask, request, jsonify,session
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity,unset_jwt_cookies, jwt_required, JWTManager
from flask import Blueprint
from db import DataBase
import mysql.connector
import json
from passlib.hash import sha256_crypt   
from datetime import datetime as dt

addCourseDetailsBlueprint = Blueprint('addCourseDetailsBlueprint',__name__)

dbInfo = DataBase()

# Route for register user details
@addCourseDetailsBlueprint.route('/course/addDetails',methods=['POST'])
@jwt_required()
def addCourseDetails():
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
                dbInfo.createCourseTable()
                courseName=data["courseName"]
                mode=data["mode"]
                if mode=="private":
                    mode=1
                    startTime=data["startTime"]
                    endTime=data["endTime"]
                    noOfQuestion=data["noOfQuestion"]
                    duration=data["duration"]
                    tabSwitchLimit=data["tabSwitch"]
                    if data["webcam"]=="no":
                        webcam=0
                    else:
                        webcam=1
                    webcamLimit=data["webcamLimit"]
                    users=[]
                    createdBy=session['username']
                    createdOn=dt.utcnow()
                    createdOn=createdOn.isoformat("T")
                    createdOn=createdOn[0:23] + "Z"
                    db_cursor.execute("INSERT INTO courses (name,mode,duration,noOfQuestion,webcam,webcamLimit,tabSwitchLimit,startTime,endTime,users,createdBy,createdOn) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(courseName,mode,duration,noOfQuestion,webcam,webcamLimit,tabSwitchLimit,startTime,endTime,json.dumps(users),createdBy,createdOn))
                    db.commit()
                else:
                    mode=0
                    createdBy=session['username']
                    createdOn=dt.utcnow()
                    db_cursor.execute("INSERT INTO courses (name,mode,createdBy,createdOn) VALUES (%s,%s,%s,%s)",(courseName,mode,createdBy,createdOn))
                    db.commit()
                return jsonify({
                    "message":"Course Added Successfully",
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