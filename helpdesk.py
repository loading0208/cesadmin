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

helpdesk = Blueprint('helpdesk',__name__)


@helpdesk.route("/helpdesk")
def Helpdesk():
    if "username" not in session:
        return render_template("/login.html")

    part = "helpdesk"
    employee = session['employeeID']
    try:
        con.connect()
        cur = con.cursor()
        sql = "SELECT * FROM db_helpdesk ORDER BY db_id DESC "
        cur.execute(sql)
        rows = cur.fetchall()
        sql = "SELECT * FROM db_department "
        cur.execute(sql)
        dep = cur.fetchall()

        return render_template('/helpdesk.html',part=part,datas = rows,dep = dep,month=month,employee=noti.Employee(),notification=noti.Notification())
    except Exception as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        con.close()


@helpdesk.route("/notifyhelpdesk")
def Notifyhelpdesk():
    if "username" not in session:
        return render_template("/login.html")
    if session['level'] != 'admin':
        return redirect(url_for('admin.Profile'))
    try:
        con.connect()
        cur = con.cursor()
        sql = "SELECT * FROM db_helpdesk WHERE jobstatus = 0 ORDER BY db_id DESC "
        cur.execute(sql)
        datas = cur.fetchall()
        if len(datas) == 0 :
            return redirect(url_for('helpdesk.Helpdesk'))
        return render_template('/notifyhelpdesk.html',month=month,datas=datas,now=datenow.strftime("%d/%m/%Y %H:%M"),employee=noti.Employee(),notification=noti.Notification())
    except Exception as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        con.close()


@helpdesk.route("/notifywaithelpdesk")
def Notifywaithelpdesk():
    if "username" not in session:
        return render_template("/login.html")
    if session['level'] != 'admin':
        return redirect(url_for('admin.Profile'))
    try:
        con.connect()
        cur = con.cursor()
        sql = "SELECT * FROM db_helpdesk WHERE jobstatus = 2 ORDER BY db_id DESC "
        cur.execute(sql)
        datas = cur.fetchall()
        if len(datas) == 0 :
            return redirect(url_for('helpdesk.Helpdesk'))
        return render_template('/notifywaithelpdesk.html',month=month,datas=datas,now=datenow.strftime("%d/%m/%Y %H:%M"),employee=noti.Employee(),notification=noti.Notification())
    except Exception as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        con.close()





@helpdesk.route("/walkietalkie")
def Walkietalkie():
    if "username" not in session:
        return render_template("/login.html")
    try:
        con.connect()
        cur = con.cursor()
        sql = "SELECT * FROM db_walkietalkie"
        cur.execute(sql)
        rows = cur.fetchall()
        return render_template('walkietalkie.html',datas = rows)
    except Exception as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        con.close()





@helpdesk.route("/addrepair", methods=["POST"])
def addrepair():
     if request.method == "POST":
# Save img ---------------------------------------------------------------------
         file = request.files['file']
         upload_folder = 'static/imghelpdesk'
         app_folder = os.path.dirname(__file__)
         img_folder = os.path.join(app_folder,upload_folder)
         try: ## เลือกรูป
             file.save(os.path.join(img_folder,file.filename))
             path = upload_folder + "/" + file.filename
         except:## ไม่เลือก รูป
             path = ""
         ##input
         fname = request.form["fname"]
         lname = request.form["lname"]
         department = request.form["depart"]
         email = request.form["email"]
         goods = request.form["goods"]
         goodsohter = request.form["goodsohter"]
         code = request.form["code"]
         detail = request.form["detail"]
         jobstatus = request.form["jobstatus"]
         telin = request.form["telin"]
         myemployeeID = request.form["myemployeeID"]
         if goods == "other":
             try:
                 con.connect()
                 cur = con.cursor()
                 sql = "insert into db_helpdesk (db_fname,db_lname,db_department,db_email,db_goods,db_code,db_detail,db_pic,jobstatus,db_telin,my_employeeID) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                 cur.execute(sql,(fname,lname,department,email,goodsohter,code,detail,path,jobstatus,telin,myemployeeID))
                 con.commit()
                 #----แจ้งเตือนผ่านไลน์--------------------------------------------
                 #token = '6j9FngK4ptn4FJB1MKPMaPPEYDEVicMhW3apbkY2O2O'
                 #messenger = Sendline(token)
                 #messenger.sendtext('คุณ' + session['fname']+' '+ 'แจ้งว่า' + detail)
                #----สิ้นสุด----------------------------------------------------
                 flash("แจ้งซ่อมสำเร็จ")
                 return redirect(url_for('helpdesk.Helpdesk'))
             except Exception as e:
                 print(e)
             finally:
                 print("Close")
                 cur.close()
                 con.close()
         else:
            try:

                 con.connect()
                 cur = con.cursor()
                 sql = "insert into db_helpdesk (db_fname,db_lname,db_department,db_email,db_goods,db_code,db_detail,db_pic,jobstatus,db_telin,my_employeeID) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                 cur.execute(sql,(fname,lname,department,email,goods,code,detail,path,jobstatus,telin,myemployeeID))
                 con.commit()
                 #----แจ้งเตือนผ่านไลน์--------------------------------------------
                 #token = '6j9FngK4ptn4FJB1MKPMaPPEYDEVicMhW3apbkY2O2O'
                 #messenger = Sendline(token)
                 #messenger.sendtext('คุณ' + session['fname']+' '+ 'แจ้งว่า' + detail)
                #----สิ้นสุด----------------------------------------------------
                 flash("แจ้งซ่อมสำเร็จ")
                 return redirect(url_for('helpdesk.Helpdesk'))
            except Exception as e:
                print(e)
            finally:
                 print("Close")
                 cur.close()
                 con.close()


@helpdesk.route("/ithelpdesk",methods=["POST"])
def Ithelpdesk():
    if request.method == "POST":
        id = request.form["id"]
        feedback = request.form["feedback"]
        Dateaccept = request.form["Dateaccept"]
        ituser = request.form["ituser"]
        jobstatus = request.form["jobstatus"]
        email = request.form["email"]
        nameuser = request.form["nameuser"]
        detail = request.form["detail"]
        try:
            con.connect()
            cur = con.cursor()
            sql = "UPDATE `db_helpdesk` SET `db_status` =%s,`dateacc` =%s,`db_it` =%s, `jobstatus` =%s, `db_email`=%s  WHERE `db_id`=%s"
            cur.execute(sql,(feedback,Dateaccept,ituser,jobstatus,email,id))
            con.commit()
            cur.close()
#----แจ้งผลผ่าน e-mail----------------------------------------------------------------------------------
            def sendthai(sendto,subj,detail):

            	myemail = 'ces-eservice@hotmail.com'
            	mypassword = '$Supportces65$'
            	receiver = sendto

            	msg = MIMEMultipart('alternative')
            	msg['Subject'] = subj
            	msg['From'] = 'IT Support CES'
            	msg['To'] = receiver
            	html = detail

            	part1 = MIMEText(html, 'html')
            	msg.attach(part1)

            	s = smtplib.SMTP('smtp-mail.outlook.com:587')
            	s.ehlo()
            	s.starttls()

            	s.login(myemail, mypassword)
            	s.sendmail(myemail, receiver.split(','), msg.as_string())
            	s.quit()

            subject = 'แจ้งผลการซ่อม'
            msg = f"""
                        <html>

                            <head></head>
                            <body style="font-family:'Prompt', sans-serif;font-size:20px;color:#079992">
                                <h2>รายงานผลการซ่อม </h2>
                                <h3>เรียนคุณ {nameuser}</h3>
                                <h3>อ้างอิงใบแจ้งซ่อมที่ : {id}</h3>
                                <h3>แจ้งว่า : {detail}</h3>
                                <h3>ผลการซ่อม : {feedback}</h3>
                                <h3>ผู้ซ่อม : {ituser}</h3>
                                <hr style="color:#079992">
                                <h3>IT Support CES</h3>
                                <a href="http://ceseservice.dyndns.org:88/" style="color:#079992" >CES-ESERVICE</a>
                            </body>
                        </html>
                    """

            sendthai(email,subject,msg)
#-----------------------------------------------------------------------------------------------------------
            con.connect()
            cur = con.cursor()

            sql = "SELECT * FROM db_helpdesk WHERE jobstatus = 0 "
            cur.execute(sql)
            new = cur.fetchall()
            if len(new) != 0:
                return redirect(url_for('helpdesk.Notifyhelpdesk'))
            return redirect(url_for('helpdesk.Helpdesk'))

            sql = "SELECT * FROM db_helpdesk WHERE jobstatus = 2 "
            cur.execute(sql)
            wait = cur.fetchall()
            if len(wait) != 0:
                return redirect(url_for('helpdesk.Notifywaithelpdesk'))
            return redirect(url_for('helpdesk.Helpdesk'))
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()



@helpdesk.route("/myjob" ,methods=["POST"])
def Myjob():
    if "username" not in session:
        return render_template("/login.html")
    if request.method == "POST":
        fname = request.form["fname"]
        try:
            con.connect()
            cur = con.cursor()
            sql = "SELECT * FROM db_helpdesk WHERE db_fname = %s"
            cur.execute(sql,(fname))
            rows = cur.fetchall()
            return render_template('helpdeskid.html',datas = rows)
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()



@helpdesk.route("/delete",methods=["POST"])
def Deletejob():
    if request.method == "POST":
        id = request.form["id"]
        try:
            con.connect()
            cur = con.cursor()
            sql = "delete from db_helpdesk where db_id = %s"
            cur.execute(sql,(id))
            con.commit()
            return redirect(url_for('helpdesk.Helpdesk'))
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()


@helpdesk.route("/report",methods=['POST'])
def Report():
    if "username" not in session:
        return render_template("/login.html")
    if session['level'] != 'admin':
        return redirect(url_for('admin.Profile'))
    if request.method == "POST":
        months = request.form['months']
        dstart = request.form['dstart']
        dend = request.form['dend']
        try:
            con.connect()
            cur = con.cursor()
            cur.execute(f"SELECT * FROM db_helpdesk where db_date between '{dstart} 00:00:00' and  '{dend} 23:59:59' ")
            rows = cur.fetchall()
            return render_template("report.html",datas = rows,months=months)
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()
