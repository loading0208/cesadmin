from flask import Flask,render_template,session,redirect,send_from_directory,request,url_for,Blueprint,flash
import os
###########################################################
import pymysql
from config import *
con = pymysql.connect(HOST,USER,PASS,DATABASE)
conn = pymysql.connect(HOSTpost,USERpost,PASSpost,DATABASEpost)
###########################################################
import noti
###########################################################
from datetime import datetime
from pythainlp.util import thai_strftime
fmt = "%B"
datenow = datetime.today()
month = thai_strftime(datenow,fmt)
###########################################################


index = Blueprint('index',__name__)

@index.route('/home')
def Home():
    if "username" not in session:
        return render_template("/login.html")
    employee = session['employeeID']
    try:
        conn.connect()
        cur = conn.cursor()
        sql = "select * from blog order by id desc"
        cur.execute(sql)
        post = cur.fetchall()

        cur.execute("select * from blog where new_status = 2 order by id desc")
        guidenew = cur.fetchall()
        return render_template('/home.html',guidenew=guidenew,month=month,post=post,employee=noti.Employee(),notification=noti.Notification())
    except Exception as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        conn.close()



@index.route('/writenews')
def Writenews():
    if "username" not in session:
        return render_template("/login.html")
    notification=noti.Notification()
    notification = notification[8][6]
    if notification != 1:
        return redirect(url_for('index.Home'))
    return render_template("writenews.html",part = "writenews",month=month,employee=noti.Employee(),notification=noti.Notification())



@index.route("/post",methods = ["POST","GET"])
def Post():
    if request.method == "POST":
        name = request.form['name']
        employeeid = request.form['employeeid']
        subject = request.form['subject']
        title = request.form['title']
        editordata = request.form['editordata']
        if editordata == '':
            flash("กรุณาเพื่มรายละเอียดของข่าวสาร")
            return redirect(url_for('index.Writenews'))
        new_status = request.form['new_status']
    try:
        conn.connect()
        cur = conn.cursor()
        sql = "insert into blog (name_write,employeeid_write,subject,title,blog_post,new_status) VALUES(%s,%s,%s,%s,%s,%s)"
        cur.execute(sql,(name,employeeid,subject,title,editordata,new_status))
        conn.commit()
        return redirect(url_for('index.Home'))
    except Exception as e:
        print (e)
    finally:
        print("Colse")
        cur.close()
        conn.close()



@index.route("/news",methods = ["POST","GET"])
def News():
    if "username" not in session:
        return render_template("/login.html")
    if request.method == "POST":
        id = request.form['id']
        try:
            conn.connect()
            cur = conn.cursor()
            sql = f"select * from blog where id = '{id}'"
            cur.execute(sql)
            row = cur.fetchall()
            return render_template("readnews.html",row=row,month=month,employee=noti.Employee(),notification=noti.Notification())
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            conn.close()
