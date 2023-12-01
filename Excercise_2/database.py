import json
import mysql.connector
import os

from dotenv import load_dotenv 
from fastapi import FastAPI
from models import User, Context

load_dotenv()

env = {
    "HOST" : os.environ.get('HOST'),
    "USER" : os.environ.get('USER'),
    "PASSWORD" : os.environ.get('PASSWORD'),
    "DATABASE" : os.environ.get('DATABASE')
}

app = FastAPI()

def connection():

    mydb = mysql.connector.connect(host=env["HOST"], user=env["USER"], password=env["PASSWORD"], database=env["DATABASE"])

    return mydb

@app.post("/is-user")
def isUser(user:User):

    mydb = connection()
    mycursor = mydb.cursor()

    sql = f"SELECT COUNT(user_id) FROM CHAT_HISTORY WHERE user_id = {user.id};"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    
    exist = True if myresult[0][0] == 1 else False

    mydb.close()

    return exist

@app.post("/save-message")   
def saveMessage(context:Context):

    mydb = connection()
    mycursor = mydb.cursor()

    sql = f"INSERT INTO CHAT_HISTORY(user_id,content,role,date) VALUES ('{context.user.id}','{context.content}', '{context.role}', NOW());"
    mycursor.execute(sql)
    mydb.commit()

    mydb.close()

@app.post("/get-messages")
def getMessages(user:User):

    mydb = connection()
    mycursor = mydb.cursor()

    sql = f"SELECT role, content FROM CHAT_HISTORY WHERE user_id = '{user.id}' ORDER BY date ASC;"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    mydb.close()

    return json.dumps(myresult)