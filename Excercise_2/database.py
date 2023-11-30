
from fastapi import FastAPI
import mysql.connector
from models import User, Context




app = FastAPI()

def connection():

    mydb = mysql.connector.connect(host="localhost", user="root", password="", database="openai")

    return mydb

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

def getMessages(user:User):

    mydb = connection()
    mycursor = mydb.cursor()

    sql = f"SELECT content FROM CHAT_HISTORY WHERE user_id = '{user.id}' ORDER BY date ASC;"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    mydb.close()

    return myresult