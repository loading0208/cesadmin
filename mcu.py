from flask import Blueprint,render_template,request,redirect,url_for,session,flash
import os
###########################################################
from datetime import datetime
from datetime import date
###########################################################
import roles
import noti
###########################################################
import pymysql
from config import *
con = pymysql.connect(HOST,USER,PASS,DATABASE)
###########################################################
from pythainlp.util import thai_strftime
fmt = "%B"
datenow = datetime.today()
month = thai_strftime(datenow,fmt)

date = date.today()

mcu = Blueprint('mcu',__name__)

@mcu.route('/mcu')
def Mcu():
    if "username" not in session:
        return render_template("/login.html")
    permissions = roles.Checkpermissions()
    permissions = permissions[0]
    if permissions[8] != 1:
        return redirect(url_for('admin.Profile'))
    try:
        con.connect()
        cur = con.cursor()
        sql = f"SELECT db_contact.con_employee_ID,db_contact.con_name,db_contact.con_position,db_contact.con_depid,db_mcu.*,db_covid.* FROM db_contact INNER JOIN (db_mcu INNER JOIN db_covid ON db_mcu.employeeID=db_covid.employeeID) ON db_contact.con_employee_ID = db_mcu.employeeID GROUP BY con_name"
        cur.execute(sql)
        alluserroles =cur.fetchall()
        return render_template("mcu.html",alluserroles=alluserroles,month=month,employee=noti.Employee(),notification=noti.Notification(),permissions=roles.Checkpermissions(),part='mcu')
    except Exception as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        con.close()



@mcu.route('/editcovid',methods=['POST'])
def Editcovid():
    if request.method == 'POST':
        employeeid = request.form['employeeid']
        date = request.form['date']
        try:
            con.connect()
            cur = con.cursor()
            sql = ("SELECT max(needle) FROM db_covid WHERE employeeID = %s")
            cur.execute(sql,(employeeid))
            chkneedle = cur.fetchall()
            chkneedle = chkneedle[0]
            chkneedle = chkneedle[0]+1
            sql = ("INSERT INTO db_covid (employeeID,needle,date_covid) VALUES(%s, %s, %s)")
            cur.execute(sql,(employeeid,chkneedle,date))
            con.commit()
            return redirect(url_for('admin.Profile'))
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()
