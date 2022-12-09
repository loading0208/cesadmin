from flask import Blueprint,render_template,request,redirect,url_for,session,flash
import os
###########################################################
from datetime import datetime
from datetime import date
###########################################################
import noti
###########################################################
import pymysql
from config import *
con = pymysql.connect(HOST,USER,PASS,DATABASE)
###########################################################

roles = Blueprint('roles',__name__)

@roles.route('/permissions', methods=['POST'])
def Permissions():
    if request.method == "POST":
        employeeID = request.form['employeeID']
        check = request.form["check"]
        reviewleave = request.form["reviewleave"]
        approveleave = request.form['approveleave']
        bookingroom = request.form['bookingroom']
        write_post = request.form['write_post']
        inbox = request.form['inbox']
        try:
            con.connect()
            cur = con.cursor()
            sql = "UPDATE role SET check_leave=%s,reviewleave=%s,approveleave=%s,meetingroom=%s,write_post=%s,comment_inbox=%s WHERE usr_employee_ID=%s"
            cur.execute(sql,(check,reviewleave,approveleave,bookingroom,write_post,inbox,employeeID))
            con.commit()
            return redirect(url_for('user.Roles'))
        except Exception as e:
            print (e)
        finally:
            print("Close")
            cur.close()
            con.close()


def Checkpermissions():
    employee = session['employeeID']
    try:
        con.connect()
        cur = con.cursor()
        sql = f"SELECT * FROM role WHERE usr_employee_ID = '{employee}'"
        cur.execute(sql)
        rolecheckid = cur.fetchall()
        return rolecheckid
    except Exception as e:
        print(e)
    finally:
        cur.close()
        con.close()
