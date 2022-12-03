from flask import Blueprint,session
import pymysql
from config import *
con = pymysql.connect(HOST,USER,PASS,DATABASE)

noti = Blueprint('noti',__name__)

def Notification():
    name = session['fname'] + ' ' + session['lname']
    employee = session['employeeID']
    department = session['department']
    level = session['level']

    try:
        con.connect()
        cur = con.cursor()
        rolesql = f"SELECT * FROM role WHERE usr_employee_ID = '{employee}' "
        cur.execute(rolesql)
        role = cur.fetchall()
        role2 =role[0][2]
        sql = f'''
                    SELECT *
                    from db_leave
                    WHERE head_employeeID = '{employee}' AND lea_status = 0
                    or manager_employeeID = '{employee}' AND lea_status = 1
                    or lea_status = 2 AND '{department}' = 'Human Resources' AND '{role2}' = 1
                '''
        cur.execute(sql)
        myreview = cur.fetchall()
        myreview = len(myreview)

        sql = f"SELECT * FROM db_helpdesk WHERE jobstatus = 0 AND '{level}' = 'admin' "
        cur.execute(sql)
        newdesk = cur.fetchall()
        snewdesk = len(newdesk)

        sql = f"SELECT * FROM db_helpdesk WHERE jobstatus = 2 AND '{level}' = 'admin'"
        cur.execute(sql)
        waitdesk = cur.fetchall()
        swaitdesk = len(waitdesk)

        sql = f"SELECT * FROM tb_user WHERE usr_status = 0 AND '{level}' = 'admin'"
        cur.execute(sql)
        nuser = cur.fetchall()
        suser = len(nuser)

        rolebooking = f"SELECT * FROM role WHERE usr_employee_ID = '{employee}' "
        cur.execute(rolebooking)
        bookingrole = cur.fetchall()
        bookingrole =bookingrole[0][5]
        print(bookingrole)
        sql = f'''SELECT * FROM db_booking WHERE bk_status = 0 or bk_status = 2 AND '{bookingrole}' = 1 '''
        cur.execute(sql)
        booing = cur.fetchall()
        sbooing = len(booing)
        sumnoti = str(myreview+snewdesk+swaitdesk+suser+sbooing)

        return sumnoti,myreview,snewdesk,swaitdesk,suser,sbooing
    except Exception as e:
        print(e)
    finally:
        cur.close()
        con.close()





def Employee():
    employee = session['employeeID']
    try:
        con.connect()
        cur = con.cursor()
        sql = f"SELECT * from db_contact WHERE con_employee_ID = '{employee}' "
        cur.execute(sql)
        employee = cur.fetchall()

        return employee
    except Exception as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        con.close()
