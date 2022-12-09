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

contacts = Blueprint('contacts',__name__)

@contacts.route('/contact')
def Contact():
    if "username" not in session:
        return render_template("/login.html")
    part = "contact"
    try:
        con.connect()
        cur = con.cursor()
        sql = f"SELECT * from db_contact "
        cur.execute(sql)
        contact = cur.fetchall()

        sql = f"SELECT * from db_department "
        cur.execute(sql)
        department = cur.fetchall()

        users = list(range(len(contact)))
        total = len(contact)

        page,per_page,offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
        #'C:\\Python38-32\\lib\\site-packages\\flask_paginate\\__init__.py'> แก้ตรงนี้ด้วย บรรทัด 267
        getuser = users[offset:offset+12]
        pagination_users = getuser
        pagination = Pagination(page=page,per_page=per_page,total=total,css_framework='bootstrap4')

        return render_template('/contact.html',part=part,department=department,month=month,contact=contact,employee=noti.Employee(),notification=noti.Notification(),permissions=roles.Checkpermissions(),
        users=pagination_users,page=page,per_page=per_page,pagination=pagination,len=total)
    except Exception as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        con.close()


@contacts.route('/search',methods=["POST"])
def Search():
    if request.method == 'POST':
        search = request.form['search']
        if search == '':
            return redirect(url_for('contacts.Contact'))
        try:
            con.connect()
            cur = con.cursor()
            sql = f"SELECT * from db_contact WHERE con_name LIKE '%{search}%' "
            cur.execute(sql)
            contact = cur.fetchall()
            if len(contact) == 0:
                flash("ไม่พบข้อมูล")
                return redirect(url_for('contacts.Contact'))
            return render_template('/searchcontact.html',part="contact",month=month,contact=contact,employee=noti.Employee(),notification=noti.Notification(),permissions=roles.Checkpermissions())
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()

@contacts.route('/addcontacts')
def Addcontacts():
    if "username" not in session:
        return render_template("/login.html")
    if session['level'] != 'admin':
        return redirect(url_for('admin.Profile'))
    try:
        con.connect()
        cur = con.cursor()
        sql = f"SELECT * from db_department "
        cur.execute(sql)
        dep = cur.fetchall()

        sql = f"SELECT * from line_group "
        cur.execute(sql)
        linegroup = cur.fetchall()

        return render_template("/addcontact.html",part="contact",month=month,dep=dep,linegroup=linegroup,employee=noti.Employee(),notification=noti.Notification(),permissions=roles.Checkpermissions())
    except Exception as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        con.close()


@contacts.route('/addcontact',methods=["POST"])
def Addcontact():
    if request.method == 'POST':
        employeeid = request.form['employeeid']
        try:
            con.connect()
            cur = con.cursor()
            sql = "SELECT con_employee_ID FROM db_contact WHERE con_employee_ID = %s"
            cur.execute(sql,(employeeid))
            checkid = cur.fetchall()
            if len(checkid) > 0:
                flash("รหัสพนักงานซ้ำ")
                return redirect(url_for('contacts.Addcontacts'))
        except Exception as e:
               print(e)
        finally:
               print("Close")
               cur.close()
               con.close()

# Save img ---------------------------------------------------------------------
        file = request.files['file']
        upload_folder = 'static/leavefile'
        app_folder = os.path.dirname(__file__)
        img_folder = os.path.join(app_folder,upload_folder)
        try: ## เลือกรูป
            file.save(os.path.join(img_folder,file.filename))
            path = upload_folder + "/" + file.filename
        except:## ไม่เลือก รูป
            path = ""
         ##input

        name = request.form['name']
        phone = request.form['phone']
        position = request.form['position']
        department = request.form['department']
        linegroup = request.form['linegroup']
        telin = request.form['telin']
        email = request.form['email']
        datestart = request.form['datestart']
        prosonal_leave = request.form['prosonal_leave']
        prosonal_leaveh = request.form['prosonal_leaveh']
        vacation_leave = request.form['vacation_leave']
        vacation_leaveh = request.form['vacation_leaveh']
        sick_leave = request.form['sick_leave']
        sick_leaveh = request.form['sick_leaveh']
        check = request.form["check"]
        reviewleave = request.form["reviewleave"]
        approveleave = request.form['approveleave']
        write_post = request.form['write_post']
        #-----------for tb_user
        status = request.form["status"]
        level = request.form["level"]
        id = request.form["id"]
        #---------------------------------
        try:
            con.connect()
            cur = con.cursor()
            sql = f'''INSERT INTO db_contact
                    (img_profile,con_name,con_tel,con_position,con_depid,line_group,con_ext,con_email,con_employee_ID,prosonal_leave,prosonal_leave_h,vacation_leave,vacation_leave_h,sick_leave,sick_leave_h,permission,startdate)
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    '''
            cur.execute(sql,(path,name,phone,position,department,linegroup,telin,email,employeeid,prosonal_leave,prosonal_leaveh,vacation_leave,vacation_leaveh,sick_leave,sick_leaveh,check,datestart))
            con.commit()
            #permission
            sql = "INSERT INTO role (usr_employee_ID,check_leave,reviewleave,approveleave,write_post) VALUES(%s,%s,%s,%s,%s)"
            cur.execute(sql,(employeeid,check,reviewleave,approveleave,write_post))
            con.commit()
            #update status user
            sql = "UPDATE tb_user SET usr_status=%s,usr_level=%s WHERE usr_id=%s"
            cur.execute(sql,(status,level,id))
            con.commit()

            return redirect(url_for('contacts.Contact'))
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()
