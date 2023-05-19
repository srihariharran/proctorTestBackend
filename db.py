import mysql.connector
import json

class DataBase:
    def __init__(self): 
        self.mysql_host='127.0.0.1'
        self.mysql_user="root"
        self.mysql_password=""
        self.database="proctorTest"

    # Check Database Exists
    def checkDatabaseExists(self):
        try:
            db = mysql.connector.connect(host=self.mysql_host,user=self.mysql_user,password=self.mysql_password)
            db_cursor = db.cursor()
        except Exception as e:
            return {
                "message":str(e),
                "status":False
            }
        try:
            result=db_cursor.execute("SHOW DATABASES LIKE 'proctorTest'").fetchall()[0][0]
            db_cursor.close()
            if result:
                return {
                "message":"database exists",
                "status":True
            }
            else:
                return {
                    "message":"database not exists",
                    "status":False
                }
        except Exception as e:
            return {
                "message":str(e),
                "status":False
            }

    # Create Database
    def createDatabase(self):
        try:
            db = mysql.connector.connect(host=self.mysql_host,user=self.mysql_user,password=self.mysql_password)
            db_cursor = db.cursor()
        except Exception as e:
            return {
                "message":str(e),
                "status":False
            }
        try:
            dbDetail=self.checkDatabaseExists()
           
            
            if(not (dbDetail['status'])):
                db_cursor.execute("CREATE DATABASE "+self.database)
                db.commit()
                db_cursor.close()
                return {
                    "message":"database created successfully",
                    "status":True
                }
        except Exception as e:
            return {
                "message":str(e),
                "status":False
            }

    #  Check User Table Exists
    def checkUserTableExists(self):
        try:
            db = mysql.connector.connect(host=self.mysql_host,user=self.mysql_user,password=self.mysql_password,database=self.database)
            db_cursor = db.cursor()
        except Exception as e:
            return {
                "message":str(e),
                "status":False
            }
        try:
            result=db_cursor.execute("SHOW TABLES LIKE 'user'").fetchall()[0][0]
            if result:
                return {
                "message":"table exists",
                "status":True
            }
            else:
                return {
                    "message":"table not exists",
                    "status":False
                }
        except Exception as e:
            return {
                "message":str(e),
                "status":False
            }

    # Create User Table
    def createUserTable(self):
        try:
            dbDetail=self.checkDatabaseExists()
            if(not (dbDetail['status'])):
                db = mysql.connector.connect(host=self.mysql_host,user=self.mysql_user,password=self.mysql_password,database=self.database)
                db_cursor = db.cursor()
            else:
                self.createDatabase()
        except Exception as e:
            return {
                "message":str(e),
                "status":False
            }
        try:
            tbDetail=self.checkUserTableExists()
            if(not (tbDetail['status'])):
                db_cursor.execute("CREATE TABLE user (username varchar(50) NOT NULL,password TEXT NOT NULL,name varchar(30) NOT NULL,organisation TEXT NOT NULL,designation varchar(100) NOT NULL,mobile varchar(50) NOT NULL,createdOn TEXT NOT NULL,lastUpdated TEXT DEFAULT NULL, PRIMARY KEY (username),UNIQUE (mobile)) ")
                db.commit()
                db_cursor.close()
                return {
                    "message":"table create successfully",
                    "status":True
                }

        except Exception as e:
            return {
                "message":str(e),
                "status":False
            }


    #  Check Course Table Exists
    def checkCourseTableExists(self):
        try:
            db = mysql.connector.connect(host=self.mysql_host,user=self.mysql_user,password=self.mysql_password,database=self.database)
            db_cursor = db.cursor()
        except Exception as e:
            return {
                "message":str(e),
                "status":False
            }
        try:
            result=db_cursor.execute("SHOW TABLES LIKE 'courses'").fetchall()[0][0]
            if result:
                return {
                "message":"table exists",
                "status":True
            }
            else:
                return {
                    "message":"table not exists",
                    "status":False
                }
        except Exception as e:
            return {
                "message":str(e),
                "status":False
            }

    # Create Course Table
    def createCourseTable(self):
        try:
            dbDetail=self.checkDatabaseExists()
            if(not (dbDetail['status'])):
                db = mysql.connector.connect(host=self.mysql_host,user=self.mysql_user,password=self.mysql_password,database=self.database)
                db_cursor = db.cursor()
            else:
                self.createDatabase()
        except Exception as e:
            return {
                "message":str(e),
                "status":False
            }
        try:
            tbDetail=self.checkCourseTableExists()
            if(not (tbDetail['status'])):
                db_cursor.execute("CREATE TABLE courses (id int NOT NULL AUTO_INCREMENT,name TEXT NOT NULL,mode int(10) DEFAULT 0,duration int(10) DEFAULT 30,noOfQuestion int(10) DEFAULT 30,webcam int(10) DEFAULT 0,webcamLimit int(10) DEFAULT 10,tabSwitchLimit int(10) DEFAULT 10,startTime TEXT DEFAULT NULL,endTime TEXT DEFAULT NULL,users json DEFAULT NULL,createdBy varchar(50) NOT NULL,createdOn TEXT NOT NULL,lastUpdated TEXT DEFAULT NULL, PRIMARY KEY (id),UNIQUE (name)) ")
                db.commit()
                db_cursor.close()
                return {
                    "message":"table create successfully",
                    "status":True
                }

        except Exception as e:
            return {
                "message":str(e),
                "status":False
            }


    #  Check Question Table Exists
    def checkQuestionTableExists(self,tb_name):
        try:
            db = mysql.connector.connect(host=self.mysql_host,user=self.mysql_user,password=self.mysql_password,database=self.database)
            db_cursor = db.cursor()
        except Exception as e:
            return {
                "message":str(e),
                "status":False
            }
        try:
            db_cursor.execute("SHOW TABLES LIKE '"+tb_name+"'")
            result=db_cursor.fetchall()[0][0]
            if result:
                return {
                "message":"table exists",
                "status":True
            }
            else:
                return {
                    "message":"table not exists",
                    "status":False
                }
        except Exception as e:
            return {
                "message":str(e),
                "status":False
            }

    # Create Question Table
    def createQuestionTable(self,tb_name):
        try:
            dbDetail=self.checkDatabaseExists()
            if(not (dbDetail['status'])):
                db = mysql.connector.connect(host=self.mysql_host,user=self.mysql_user,password=self.mysql_password,database=self.database)
                db_cursor = db.cursor()
            else:
                self.createDatabase()
        except Exception as e:
            return {
                "message":str(e),
                "status":False
            }
        try:
            tbDetail=self.checkQuestionTableExists(tb_name)
            if(not (tbDetail['status'])):
                db_cursor.execute("CREATE TABLE "+tb_name+" (id int NOT NULL AUTO_INCREMENT,question TEXT NOT NULL,options json DEFAULT NULL,correctAnswer TEXT DEFAULT NULL,createdBy varchar(50) NOT NULL,createdOn TEXT NOT NULL,lastUpdated TEXT DEFAULT NULL, PRIMARY KEY (id),UNIQUE (question)) ")
                db.commit()
                db_cursor.close()
                return {
                    "message":"table create successfully",
                    "status":True
                }

        except Exception as e:
            return {
                "message":str(e),
                "status":False
            }


    #  Check Test Report Table Exists
    def checkTestReportTableExists(self,tb_name):
        try:
            db = mysql.connector.connect(host=self.mysql_host,user=self.mysql_user,password=self.mysql_password,database=self.database)
            db_cursor = db.cursor()
        except Exception as e:
            return {
                "message":str(e),
                "status":False
            }
        try:
            db_cursor.execute("SHOW TABLES LIKE '"+tb_name+"'")
            result=db_cursor.fetchall()[0][0]
            if result:
                return {
                "message":"table exists",
                "status":True
            }
            else:
                return {
                    "message":"table not exists",
                    "status":False
                }
        except Exception as e:
            return {
                "message":str(e),
                "status":False
            }

    # Create TestReport Table
    def createTestReportTable(self,tb_name):
        try:
            dbDetail=self.checkDatabaseExists()
            if(not (dbDetail['status'])):
                db = mysql.connector.connect(host=self.mysql_host,user=self.mysql_user,password=self.mysql_password,database=self.database)
                db_cursor = db.cursor()
            else:
                self.createDatabase()
        except Exception as e:
            return {
                "message":str(e),
                "status":False
            }
        try:
            tbDetail=self.checkTestReportTableExists(tb_name)
            if(not (tbDetail['status'])):
                db_cursor.execute("CREATE TABLE "+tb_name+" (id int NOT NULL AUTO_INCREMENT,questionDetails json DEFAULT NULL,tabSwitchCount int DEFAULT NULL,webcamCount int DEFAULT NULL,doubtImages json DEFAULT NULL,testDetails json DEFAULT NULL,submittedBy varchar(50) DEFAULT NULL,startedOn TEXT DEFAULT NULL,submittedOn TEXT DEFAULT NULL, PRIMARY KEY (id)) ")
                db.commit()
                db_cursor.close()
                return {
                    "message":"table create successfully",
                    "status":True
                }

        except Exception as e:
            print(e)
            return {
                "message":str(e),
                "status":False
            }

