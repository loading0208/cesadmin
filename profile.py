from flask import Flask,render_template,session,redirect,send_from_directory,request,url_for,Blueprint,flash
import os
###########################################################
import pymysql
from config import *
con = pymysql.connect(HOST,USER,PASS,DATABASE)
###########################################################
from flask_paginate import Pagination,get_page_args #แบ่งหน้าข้อมูล
###########################################################
import noti
import roles
###########################################################
from datetime import datetime
from pythainlp.util import thai_strftime
fmt = "%B"
datenow = datetime.today()
month = thai_strftime(datenow,fmt)
###########################################################

profile = Blueprint('profile',__name__)

@profile.route('/viewprofile',methods=["POST"])
def viewprofile():
    if request.method == 'POST':
        employeeid = request.form['employeeid']
        try:
            con.connect()
            cur = con.cursor()

            sql = "SELECT * FROM line_group"
            cur.execute(sql)
            linegroup = cur.fetchall()

            sql = "SELECT * FROM db_contact INNER JOIN role ON db_contact.con_employee_ID = role.usr_employee_ID INNER JOIN line_group ON db_contact.line_group=line_group.line_group_id WHERE con_employee_ID = %s"
            cur.execute(sql,(employeeid))
            profile = cur.fetchall()
            if len(profile) == 0:
                flash("เกิดข้อมผิดพลาด ไม่สามารถดูข้อมูลได้ กรุณาติดต่อ IT Support โทร 147")
                return redirect(url_for('contacts.Contact'))
            return render_template('viewprofile.html',part="contact",profile = profile,linegroup=linegroup,lprofile=len(profile),employee=noti.Employee(),notification=noti.Notification(),permissions=roles.Checkpermissions())
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()
