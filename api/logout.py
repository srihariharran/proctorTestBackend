from flask import Flask, request, jsonify, session
from flask import Blueprint
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity,unset_jwt_cookies, jwt_required, JWTManager
from db import DataBase
import json
import mysql.connector
from passlib.hash import sha256_crypt   

logoutBlueprint = Blueprint('logoutBlueprint',__name__)

dbInfo = DataBase()

# Route for register user details
@logoutBlueprint.route('/logout',methods=['POST'])
@jwt_required()
def logout():
    # Checking for Request Method
    if request.method=='POST':
        if 'cookie' in session:
            jti = get_jwt()["jti"]
            session["accessToken"]=jti
            return jsonify({
                "message":"Logout Successfull",
                "status":True
            })
        else:
            return jsonify({
                "message":"Access Denied",
                "status":False
            })
    else:
        return jsonify({
            "message":"Error! Invalid Method"
        })