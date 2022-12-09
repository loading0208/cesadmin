from flask import Blueprint,render_template,request,redirect,url_for,session,flash
import os
###########################################################
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
###########################################################
from songline import Sendline
###########################################################
import noti
import roles
############################################################
import pymysql
from config import *
con = pymysql.connect(HOST,USER,PASS,DATABASE)
###########################################################
from datetime import datetime
from pythainlp.util import thai_strftime
fmt = "%B"
datenow = datetime.today()
month = thai_strftime(datenow,fmt)

user = Blueprint('user',__name__)

@user.route("/login")
def Login():
    if "username" not in session:
        return render_template("/login.html",status="wait")
    else:
        return redirect(url_for('home.Home'))

@user.route("/sign-in")
def Signin():
    if "username" not in session:
        return render_template("/login.html")
    else:
        return redirect(url_for('home.Home'))

@user.route("/checklogin", methods=["POST"])
def Checklogin():
    username = request.form['username']
    password = request.form['password']
    try:
        con.connect()
        cur = con.cursor()
        sql = "SELECT tb_user.usr_fname,tb_user.usr_lname,tb_user.usr_email,tb_user.usr_depart,tb_user.usr_level,tb_user.usr_employee_ID,db_contact.con_name FROM tb_user INNER JOIN db_contact ON tb_user.usr_employee_ID =db_contact.con_employee_ID  WHERE tb_user.usr_username = %s AND tb_user.usr_password = %s and tb_user.usr_status = 1"
        cur.execute(sql, (username, password))
        rows = cur.fetchall()
        if len(rows) > 0:
            session['username'] = username
            session['fname'] = rows[0][0]
            session['lname'] = rows[0][1]
            session['email'] = rows[0][2]
            session['department'] = rows[0][3]
            session['level'] = rows[0][4]
            session['employeeID'] = rows[0][5]
            session['name'] = rows[0][6]
            session.permanent = True
            flash("Login successfully, welcome" )
            return redirect(url_for('admin.Profile'))
        else:
            flash("ไม่พบข้อมูลในระบบ กรุณาลองใหม่อีกครั้ง")
            return redirect(url_for('user.Signin'))
    except Exception as e:
           print(e)
    finally:
           print("Close")
           cur.close()
           con.close()

@user.route("/formforgetpassword")
def Formforgetpassword():
    return render_template("forgetpassword.html")


@user.route("/forgetpassword", methods=["POST"])
def Forgetpassword():
    if request.method == "POST":
        newpassforget = request.form["newpassforget"]
        confirenewpassforget = request.form["confirenewpassforget"]
        email = request.form["email"]
        try:
            con.connect()
            cur = con.cursor()
            sql = "SELECT * FROM tb_user WHERE usr_email = %s "
            cur.execute(sql, (email))
            rows = cur.fetchall()
            if len(rows) <= 0:
                flash("กรุณากรอก E-Mail ที่เคยลงทะเบียน")
                return redirect(url_for("user.Formforgetpassword"))
            if newpassforget != confirenewpassforget:
                flash("Password ไม่ตรงกัน")
                return redirect(url_for("user.Formforgetpassword"))
            if len(rows) > 0:
                sql = "UPDATE tb_user SET `usr_password`=%s  WHERE `usr_email`=%s"
                cur.execute(sql, (newpassforget, email))
                flash("เปลี่ยน Password เรียบร้อยครับ")
                # return redirect(url_for("user.Login"),status = "ok")
                return render_template('login.html', status="ok")
        except Exception as e:
               print(e)
        finally:
               print("Close")
               cur.close()
               con.close()



@user.route("/formregis")
def Formregis():
    try:
        con.connect()
        cur = con.cursor()
        sql = "SELECT * FROM db_department "
        cur.execute(sql)
        dep = cur.fetchall()
        return render_template("/regisuser.html",dep = dep)
    except Exception as e:
           print(e)
    finally:
           print("Close")
           cur.close()
           con.close()

@user.route("/alluser")
def Alluser():
    if "username" not in session:
        return render_template("/login.html")
    try:
        con.connect()
        cur = con.cursor()
        sql = "SELECT * FROM tb_user"
        cur.execute(sql)
        rowsalluser = cur.fetchall()
        return render_template("dashboard/alluser.html",rowsalluser = rowsalluser)
    except Exception as e:
           print(e)
    finally:
           print("Close")
           cur.close()
           con.close()


@user.route("/newuser")
def Newuser():
    if "username" not in session:
        return render_template("/login.html")
    if session['level'] != 'admin':
        return redirect(url_for('admin.Profile'))
    try:
        con.connect()
        cur = con.cursor()
        sql = "SELECT * FROM tb_user WHERE usr_status = 0"
        cur.execute(sql)
        newuser = cur.fetchall()
        return render_template("notifynewuser.html",newuser = newuser,month=month,employee=noti.Employee(),notification=noti.Notification(),permissions=roles.Checkpermissions())
    except Exception as e:
           print(e)
    finally:
           print("Close")
           cur.close()
           con.close()


@user.route("/approvenewuser",methods=["POST"])
def Approvenewuser():
    if request.method == "POST":
        id = request.form['id']
        try:
            con.connect()
            cur = con.cursor()
            sql = "SELECT * FROM db_department "
            cur.execute(sql)
            dep = cur.fetchall()

            sql = f"SELECT * from line_group "
            cur.execute(sql)
            linegroup = cur.fetchall()

            sql = "SELECT * FROM tb_user WHERE usr_id = %s"
            cur.execute(sql,(id))
            newuser = cur.fetchall()
            return render_template("approvenewuser.html",linegroup=linegroup,dep=dep,newuser = newuser,month=month,employee=noti.Employee(),notification=noti.Notification(),permissions=roles.Checkpermissions())
        except Exception as e:
               print(e)
        finally:
               print("Close")
               cur.close()
               con.close()



@user.route("/edituser",methods=["POST"])
def Edituser():
    if request.method == "POST":
        id = request.form["id"]
        fname = request.form["fname"]
        lname = request.form["lname"]
        email = request.form["email"]
        depart = request.form["depart"]
    try:
        con.connect()
        cur = con.cursor()
        sql = "UPDATE tb_user SET `usr_fname`=%s,`usr_lname`=%s,`usr_email`=%s,`usr_depart`=%s  WHERE `usr_id`=%s"
        cur.execute(sql,(fname,lname,email,depart,id))
        rowsalluser = cur.fetchall()
        return redirect(url_for('user.Alluser'))
    except Exception as e:
           print(e)
    finally:
           print("Close")
           cur.close()
           con.close()

@user.route("/deleteuser",methods=["POST"])
def Deleteuser():
    if request.method == "POST":
        id = request.form["id"]
        try:
            con.connect()
            cur = con.cursor()
            sql = "delete from tb_user where usr_id = %s"
            cur.execute(sql,(id))
            con.commit()
            return redirect(url_for("dashboard.Dashboard"))
        except Exception as e:
               print(e)
        finally:
               print("Close")
               cur.close()
               con.close()

@user.route("/regisuser", methods=["POST"])
def Regisuser():
    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        employeeid = request.form["employeeid"]

        #เช็ค employeeid ซ้ำ ---------------------------------------------
        try:
            con.connect()
            cur = con.cursor()
            sql = "SELECT usr_employee_ID FROM tb_user WHERE usr_employee_ID = %s "
            cur.execute(sql,(employeeid))
            rows = cur.fetchall()
            if len (rows) >0:
                flash("รหัสพนักงานนี้ได้ลงทะเบียนไว้แล้ว กรุณาลองใหม่ หรือ ติดต่อ 147")
                return redirect(url_for('user.Formregis'))
        except Exception as e:
               print(e)
        finally:
               print("Close")
               cur.close()
               con.close()
        #----END-----------------------------------------------------
        email = request.form["email"]
        #เช็ค e-mail ซ้ำ ---------------------------------------------
        try:
            con.connect()
            cur = con.cursor()
            sql = "SELECT * FROM tb_user WHERE usr_email = %s "
            cur.execute(sql,(email))
            rows = cur.fetchall()
            if len (rows) >0:
                flash("E-Mail นี้มีผู้ใช้งานแล้ว กรุณาลองใหม่ หรือ ติดต่อ 147")
                return redirect(url_for('user.Formregis'))
        except Exception as e:
               print(e)
        finally:
               print("Close")
               cur.close()
               con.close()
        #----END-----------------------------------------------------
        depart = request.form["depart"]
        username = request.form["username"]
        password = request.form["password"]
        repassword = request.form["repassword"]
        #--------------------เช็ค user ซ้ำ---------------------------------------------
        try:
            con.connect()
            cur = con.cursor()
            sql = "SELECT * FROM tb_user WHERE usr_username = %s "
            cur.execute(sql,(username))
            rows = cur.fetchall()
            if len (rows) >0:
                flash("Username นี้มีผู้ใช้งานแล้ว กรุณากรอกใหม่")
                return redirect(url_for('user.Formregis'))
        except Exception as e:
               print(e)
        finally:
               print("Close")
               cur.close()
               con.close()
        #------------------------สิ้นสุด-------------------------------------
        if password != repassword:
            flash("Password ไม่ตรงกัน")
            return redirect(url_for('user.Formregis'))
    try:
        con.connect()
        cur = con.cursor()
        sql = "insert into tb_user (usr_fname,usr_lname,usr_email,usr_depart,usr_username,usr_password,usr_employee_ID) values(%s,%s,%s,%s,%s,%s,%s)"
        cur.execute(sql,(fname,lname,email,depart,username,password,employeeid))
        con.commit()
        flash("สมัครสมาชิกเรียบร้อย รอ E-Mail ยืนยันเพื่อเข้าสู่ระบบ")
        #----แจ้งเตือนผ่านไลน์--------------------------------------------
        #token = '6j9FngK4ptn4FJB1MKPMaPPEYDEVicMhW3apbkY2O2O'
        #messenger = Sendline(token)
        #messenger.sendtext('มี User ใหม่รอการอนุมัติ')
        #----สิ้นสุด----------------------------------------------------
        return redirect(url_for('user.Login'))
    except Exception as e:
           print(e)
    finally:
           print("Close")
           cur.close()
           con.close()


@user.route("/logoff")
def logoff():
    session.clear()
    return redirect(url_for('user.Login'))


@user.route("/roles")
def Roles():
    if "username" not in session:
        return render_template("/login.html")
    if session['level'] != 'admin':
        return redirect(url_for('admin.Profile'))
    try:
        con.connect()
        cur = con.cursor()
        sql = "SELECT * FROM tb_user WHERE usr_status = 1"
        cur.execute(sql)
        alluserroles =cur.fetchall()
        return render_template("role.html",alluserroles=alluserroles,month=month,employee=noti.Employee(),notification=noti.Notification(),permissions=roles.Checkpermissions(),part='admin')
    except Exception as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        con.close()

@user.route("/editroleuser",methods=["POST"])
def Editroleuser():
    if "username" not in session:
        return render_template("/login.html")
    if request.method == "POST":
        userid = request.form["userid"]
    try:
        con.connect()
        cur = con.cursor()
        sql =f"SELECT tb_user.* , db_contact.img_profile,role.* FROM tb_user INNER JOIN (db_contact INNER JOIN role ON db_contact.con_employee_ID=role.usr_employee_ID) ON tb_user.usr_employee_ID=role.usr_employee_ID  WHERE tb_user.usr_employee_ID = '{userid}' "
        cur.execute(sql)
        editroleuser = cur.fetchall()

        sql = "SELECT * FROM db_department"
        cur.execute(sql)
        dep = cur.fetchall()
        return render_template("editrole.html",editroleuser=editroleuser,dep=dep,employee=noti.Employee(),notification=noti.Notification(),permissions=roles.Checkpermissions(),part='editroleuser')
    except Exception as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        con.close()
