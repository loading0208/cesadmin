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
        level = request.form['level']
        status = request.form['status']
        userroles = request.form['userroles']
        mcu = request.form['mcu']
        menuadmin= request.form['menuadmin']
        try:
            con.connect()
            cur = con.cursor()
            sql = "UPDATE role SET check_leave=%s,reviewleave=%s,approveleave=%s,meetingroom=%s,write_post=%s,comment_inbox=%s,user_roles=%s,mcu=%s,per_level=%s WHERE usr_employee_ID=%s"
            cur.execute(sql,(check,reviewleave,approveleave,bookingroom,write_post,inbox,userroles,mcu,menuadmin,employeeID))
            con.commit()

            sql_level = "UPDATE tb_user SET usr_level=%s,usr_status=%s WHERE usr_employee_ID=%s"
            cur.execute(sql_level,(level,status,employeeID))
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

@roles.route('/test')
def test():
    con.connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM log_leave")
    test = cur.fetchall()
    return render_template("test.html",test=test)

@roles.route('/deleterole', methods=['POST'])
def delete():
    if request.method == 'POST':
        test = request.form['test']
        print(test)
        con.connect()
        cur = con.cursor()
        cur.execute(f"DELETE FROM log_leave WHERE log_id = '{test}' ")
        con.commit()

        return redirect(url_for('roles.test'))
