from flask import Flask, request, jsonify, session, Response
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity,unset_jwt_cookies, jwt_required, JWTManager
from flask_cors import CORS
from db import DataBase
import json
from passlib.hash import sha256_crypt   
import random
import string
import hashlib
from datetime import datetime, timedelta, timezone
import cv2


# Importing Routes Pages
from api.registerUser import registerUserBlueprint
from api.checkMobileNoExists import checkMobileNoExistsBlueprint
from api.checkUsernameExists import checkUsernameExistsBlueprint
from api.login import loginBlueprint
from api.logout import logoutBlueprint
from api.getCourseDetails import getCourseDetailsBlueprint
from api.getQuestionDetails import getQuestionDetailsBlueprint
from api.getTestDetails import getTestDetailsBlueprint
from api.submitTestDetails import submitTestDetailsBlueprint
from api.addCourseDetails import addCourseDetailsBlueprint
from api.editCourseDetails import editCourseDetailsBlueprint
from api.deleteCourseDetails import deleteCourseDetailsBlueprint
from api.addQuestionDetails import addQuestionDetailsBlueprint
from api.editQuestionDetails import editQuestionDetailsBlueprint
from api.deleteQuestionDetails import deleteQuestionDetailsBlueprint
from api.startTestDetails import startTestDetailsBlueprint
from api.submitTestDetails import submitTestDetailsBlueprint
from api.checkFace import checkFaceBlueprint
from api.getUserDetails import getUserDetailsBlueprint
from api.getAllTestReportDetails import getAllTestReportDetailsBlueprint
from api.getTestReportDetails import getTestReportDetailsBlueprint


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "EBNcri5PYrn7H5j"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.secret_key="abc"
jwt = JWTManager(app)
CORS(app,supports_credentials=True)


dbInfo = DataBase()

startURL="/api"

app.register_blueprint(registerUserBlueprint,url_prefix=startURL)
app.register_blueprint(checkMobileNoExistsBlueprint,url_prefix=startURL)
app.register_blueprint(checkUsernameExistsBlueprint,url_prefix=startURL)
app.register_blueprint(loginBlueprint,url_prefix=startURL)
app.register_blueprint(logoutBlueprint,url_prefix=startURL)
app.register_blueprint(getCourseDetailsBlueprint,url_prefix=startURL)
app.register_blueprint(getQuestionDetailsBlueprint,url_prefix=startURL)
app.register_blueprint(getTestDetailsBlueprint,url_prefix=startURL)
app.register_blueprint(submitTestDetailsBlueprint,url_prefix=startURL)
app.register_blueprint(addCourseDetailsBlueprint,url_prefix=startURL)
app.register_blueprint(editCourseDetailsBlueprint,url_prefix=startURL)
app.register_blueprint(deleteCourseDetailsBlueprint,url_prefix=startURL)
app.register_blueprint(addQuestionDetailsBlueprint,url_prefix=startURL)
app.register_blueprint(editQuestionDetailsBlueprint,url_prefix=startURL)
app.register_blueprint(deleteQuestionDetailsBlueprint,url_prefix=startURL)
app.register_blueprint(startTestDetailsBlueprint,url_prefix=startURL)
app.register_blueprint(checkFaceBlueprint,url_prefix=startURL)
app.register_blueprint(getUserDetailsBlueprint,url_prefix=startURL)
app.register_blueprint(getAllTestReportDetailsBlueprint,url_prefix=startURL)
app.register_blueprint(getTestReportDetailsBlueprint,url_prefix=startURL)


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    if "accessToken" in session:
        token = session["accessToken"]
        session.pop("accessToken")
        return token is not None

@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.utcnow()
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["token"] = access_token 
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        
        # Case where there is not a valid JWT. Just return the original respone
        return response


@app.route('/connect',methods=['POST'])
def connect():
    try:
        letter = string.ascii_letters
        num = string.digits
        symbols = string.punctuation
        all = letter + num +symbols
        temp = random.sample(all,10)
        cookie = "".join(temp)
        session["cookie"]=hashlib.md5(cookie.encode('utf-8')).hexdigest()
        return jsonify({
            "message":"Connected",
            "status":True
        })
    except Exception as e:
        return {
            "message":str(e),
            "status":False
        }

@app.route('/disconnect',methods=['POST'])
def disconnect():
    try:
        session.clear()
        return jsonify({
            "message":"Disconnected",
            "status":True
        })
    except Exception as e:
        return {
            "message":str(e),
            "status":False
        }





if __name__ == '__main__':
   app.run(debug = True)