from flask import Flask, request, jsonify, session
from flask import Blueprint
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity,unset_jwt_cookies, jwt_required, JWTManager
from db import DataBase
import json
import mysql.connector
import cv2
from passlib.hash import sha256_crypt   

checkFaceBlueprint = Blueprint('checkFaceBlueprint',__name__)

dbInfo = DataBase()

# Route for register user details
@checkFaceBlueprint.route('/checkFace',methods=['POST'])
@jwt_required()
def checkFace():
    # Checking for Request Method
    if request.method=='POST':
        data=request.get_json()
        # print(data)
        try:

            camera = cv2.VideoCapture(data["image"])
            # while True:
            success, frame = camera.read()  # read the camera frame
            face_cascade=cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
            eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')
            faces=face_cascade.detectMultiScale(frame,1.3,4)    
        
            if len(faces)==0:
                msg="No face / Not looking screen"
            elif len(faces)==1:
                msg=""
            else:
                msg="Too many faces"
            # print("Count "+str(len(faces)))
            return jsonify({
                "count":len(faces),
                "message":str(msg),
                "status":True
            })
        except Exception as e:
            return jsonify({
                "message":str(e),
                "status":False
            })
        # eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')
        # eyes = eye_cascade.detectMultiScale(frame,1.3,5)
    else:
        return jsonify({
            "message":"Error! Invalid Method"
        })