from flask import Flask, request, jsonify,session
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity,unset_jwt_cookies, jwt_required, JWTManager
from flask import Blueprint
from db import DataBase
import mysql.connector
import json
from passlib.hash import sha256_crypt   
from datetime import datetime as dt

editCourseDetailsBlueprint = Blueprint('editCourseDetailsBlueprint',__name__)

dbInfo = DataBase()

# Route for register user details
@editCourseDetailsBlueprint.route('/course/editDetails',methods=['POST'])
@jwt_required()
def editCourseDetails():
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
            dbInfo.createCourseTable()
            courseId=data["courseId"]
            mode=data["mode"]
            lastUpdated=dt.utcnow()
            lastUpdated=lastUpdated.isoformat("T")
            lastUpdated=lastUpdated[0:23] + "Z"
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
                users=data["users"]
            
                
                db_cursor.execute("UPDATE courses SET mode=%s,duration=%s,noOfQuestion=%s,webcam=%s,webcamLimit=%s,tabSwitchLimit=%s,startTime=%s,endTime=%s,users=%s,lastUpdated=%s WHERE id=%s",(mode,duration,noOfQuestion,webcam,webcamLimit,tabSwitchLimit,startTime,endTime,json.dumps(users),lastUpdated,courseId))
                db.commit()
            else:
                mode=0
                
                db_cursor.execute("UPDATE courses SET mode=%s,lastUpdated=%s,duration='',noOfQuestion='',webcam='',webcamLimit='',tabSwitchLimit='',startTime='',endTime='',users='' WHERE id=%s",(mode,lastUpdated,courseId))
                db.commit()
            return jsonify({
                "message":"Course Modified Successfully",
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