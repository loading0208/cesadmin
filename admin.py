from flask import Blueprint,render_template,request,redirect,url_for,session,flash
import os
###########################################################
from datetime import datetime
from datetime import date
###########################################################
from dateutil.relativedelta import relativedelta #คำนวนระยะห่างของวัน
###########################################################
import roles
import noti
###########################################################
import pymysql
from config import *
con = pymysql.connect(HOST,USER,PASS,DATABASE)
###########################################################
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
###########################################################
import index
###########################################################
from pythainlp.util import thai_strftime
fmt = "%B"
datenow = datetime.today()
month = thai_strftime(datenow,fmt)


admin = Blueprint('admin',__name__)


@admin.route('/profile')
def Profile():
    if "username" not in session:
        return render_template("/login.html")
    employee = session['employeeID']
    try:
        con.connect()
        cur = con.cursor()
        sql = f"SELECT * from db_leave WHERE my_employeeID = '{employee}' ORDER BY lea_id DESC "
        cur.execute(sql)
        myleave = cur.fetchall()

        sql = f"SELECT * FROM db_helpdesk WHERE my_employeeID = '{employee}' "
        cur.execute(sql)
        myhelpdesk = cur.fetchall()

        sql = f"SELECT * FROM db_booking WHERE employeeID = '{employee}' "
        cur.execute(sql)
        booking = cur.fetchall()

        sql = f"SELECT * from borrow_db WHERE employee_ID = '{employee}' "
        cur.execute(sql)
        borrow = cur.fetchall()

        sql = f"SELECT * from db_contact WHERE con_employee_ID = '{employee}' "
        cur.execute(sql)
        employee = cur.fetchall()

        a = employee[0][18]
        z = relativedelta(date.today(),a)
        z = z.years,z.months,z.days
        y = str(z[0])
        m = str(z[1])
        d = str(z[2])
        aeg = y +' '+ 'ปี' +' '+ m + ' '+ 'เดือน'+ ' ' + d +' ' +'วัน'
        return render_template('/profile.html',month=month,myleave=myleave,smyleave=len(myleave),myhelpdesk=myhelpdesk,smyhelpdesk=len(myhelpdesk),booking=booking,sbooking=len(booking),employee=noti.Employee(),borrow=borrow,sborrow=len(borrow),notification=noti.Notification(),permissions=roles.Checkpermissions(),aeg=aeg)
    except Exception as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        con.close()


@admin.route('/leavereview')
def Leavereview():
    if "username" not in session:
        return render_template("/login.html")
    name = session['fname'] + ' ' + session['lname']
    employee = session['employeeID']
    department = session['department']
    try:
        con.connect()
        cur = con.cursor()

        permissionsql = f"SELECT * FROM role WHERE usr_employee_ID = '{employee}' "
        cur.execute(permissionsql)
        permission = cur.fetchall()
        permission =permission[0][2]

        sql = f'''
                SELECT * from db_leave
                WHERE head_employeeID = '{employee}' AND lea_status = 0
                or manager_employeeID = '{employee}' AND lea_status = 1
                or lea_status = 2 AND '{department}' = 'Human Resources' AND '{permission}' = 1 order by lea_id DESC
                '''
        cur.execute(sql)
        myreview = cur.fetchall()
        if len(myreview) == 0 :
            return redirect(url_for('admin.Profile'))
        return render_template('/review.html',month=month,myreview=myreview,employee=noti.Employee(),notification=noti.Notification(),permissions=roles.Checkpermissions())
    except Exception as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        con.close()




@admin.route('/leave')
def Leave():
    if "username" not in session:
        return render_template("/login.html")
    part = "leave"
    department = session['department']
    employee = session['employeeID']
    try:
        con.connect()
        cur = con.cursor()
        sql = f"SELECT line_group FROM db_contact WHERE con_employee_ID = '{employee}' "
        cur.execute(sql)
        linegroup = cur.fetchall()
        linegroup = linegroup[0]
        linegroup = linegroup[0]
        sql = f'''
                  SELECT con_name,con_employee_ID from db_contact WHERE con_depid = '{department}'
                  or line_group = '{linegroup}' AND con_name
                  IN (SELECT db_contact.con_name FROM role INNER JOIN db_contact ON db_contact.con_employee_ID = role.usr_employee_ID
                  WHERE approveleave = 1)
                  '''
        cur.execute(sql)
        user = cur.fetchall()

        sql = f'''
                  SELECT con_name,con_employee_ID from db_contact WHERE con_depid = '{department}'
                  or line_group = '{linegroup}' AND con_name
                  IN (SELECT db_contact.con_name FROM role INNER JOIN db_contact ON db_contact.con_employee_ID = role.usr_employee_ID
                  WHERE reviewleave = 1)
                  '''
        cur.execute(sql)
        userreviewleave = cur.fetchall()

        return render_template("/leave.html",part=part,month=month,user=user,userreviewleave=userreviewleave,employee=noti.Employee(),permissions=roles.Checkpermissions(),datenow=datenow.strftime("%d/%m/%Y"),notification=noti.Notification())
    except Exception as e:
        print(e)
    finally:
        print("Close")
        cur.close()
        con.close()


@admin.route("/addleave", methods=["POST"])
def Addleave():
    if request.method == "POST":
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
        name = request.form["name"]
        dep = request.form["dep"]
        leavetype = request.form["leavetype"]
        if leavetype == 'ลาอื่นๆ':
            leavetype = 'ลาอื่นๆ /'+' ' + request.form["leavetypeother"]
        datecreate = request.form["datecreate"]
        leavestart = request.form["leavestart"]
        leaveend = request.form["leaveend"]
        if leavestart > leaveend :
            flash("กรุณาเช็ควันที่ลา")
            return redirect(url_for('admin.Leave'))
        leavenumd = request.form["leavenumd"]
        leavenumh = request.form["leavenumh"]
        if leavenumd == '0' and leavenumh == '0.5' :
            flash("ไม่สามารถลา 0.5 ชั่วโมงได้ กรุณาทำรายการใหม่")
            return redirect(url_for('admin.Leave'))
        causedetail = request.form["causedetail"]
        headuser = request.form["headuser"]
        head = headuser.strip('(').split(",")
        headuser = (head[0])
        heademployeeID = (head[1].strip(')'))
        manageruser = request.form["manageruser"]
        manager = manageruser.strip('(').split(",")
        manageruser = (manager[0])
        manageremployeeID = (manager[1].strip(')'))
        myemployeeID = request.form["employeeid"]
        createlog = request.form["createlog"]
        try:
            con.connect()
            cur = con.cursor()
            sql = "insert into db_leave (lea_name,lea_dep,lea_type,lea_datecreate,lea_dateleave,lea_todateleave,lea_datenumd,lea_datenumh,lea_causedetail,lea_head,lea_manager,lea_file,my_employeeID,head_employeeID,manager_employeeID) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(sql,(name,dep,leavetype,datecreate,leavestart,leaveend,leavenumd,leavenumh,causedetail,headuser,manageruser,path,myemployeeID,heademployeeID,manageremployeeID))
            con.commit()

            logsql = f"SELECT max(lea_id) from db_leave"
            cur.execute(logsql)
            logsql = cur.fetchall()
            logsql = logsql[0]
            logsqladd = int(logsql[0])

            logsql = "insert into log_leave (log_lea_id,log_action,log_action_by) VALUES(%s, %s,%s)"
            cur.execute(logsql,(logsqladd,createlog,name))
            con.commit()


            qemail = f"select con_email from db_contact where con_employee_ID = '{heademployeeID}' "
            cur.execute(qemail)
            email = cur.fetchall()

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

            subject = 'ขออนุญาตลางาน'
            msg = f"""
                        <html>

                            <head></head>
                            <body style="font-family:'Prompt', sans-serif;font-size:20px;color:#079992">
                                <h2>ขออนุญาตลางาน</h2>
                                <h3>เรียนคุณ {headuser} </h3>
                                <h3>มีพนักงานภายใต้การบังคับบัญชาของท่านขอลางาน รบกวนตรวจสอบเพื่อพิจารณาด้วยครับ</h3>
                                <hr style="color:#079992">
                                <h3>CES ADMIN</h3>
                                <a href="http://ceseservice.dyndns.org:88/" style="color:#079992" >CES-ESERVICE</a>
                            </body>
                        </html>

                    """
            emailto = email[0] #ข้อมูลที่ลูปมาเป็น type tuple เลยต้องดึงค่าออกมาก่อน
            sendthai(emailto[0],subject,msg)
#-----------------------------------------------------------------------------------------------------------
            flash("ส่งใบลาสำเร็จ")
            return redirect(url_for('admin.Profile'))
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()



@admin.route("/detailleave",methods=["POST"])
def Detailleave():
    if request.method =="POST":
        id = request.form["id"]
        try:
            con.connect()
            cur = con.cursor()
            sql = "SELECT * FROM db_leave WHERE lea_id=%s"
            cur.execute(sql,(id))
            detailleave = cur.fetchall()

            sql = f"SELECT * from log_leave WHERE log_lea_id = '{id}' ORDER BY log_id DESC "
            cur.execute(sql)
            log = cur.fetchall()

            return render_template('detailleave.html',month=month,detailleave = detailleave,employee=noti.Employee(),log=log,notification=noti.Notification(),permissions=roles.Checkpermissions())
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()


@admin.route("/mydetailleave",methods=["POST"])
def Mydetailleave():
    if request.method =="POST":
        id = request.form["id"]
        try:
            con.connect()
            cur = con.cursor()
            sql = "SELECT * FROM db_leave WHERE lea_id=%s"
            cur.execute(sql,(id))
            mydetailleave = cur.fetchall()

            sql = f"SELECT * from log_leave WHERE log_lea_id = '{id}' ORDER BY log_id DESC "
            cur.execute(sql)
            log = cur.fetchall()

            return render_template('mydetailleave.html',month=month,mydetailleave = mydetailleave,employee=noti.Employee(),log=log,notification=noti.Notification(),permissions=roles.Checkpermissions(),id=id)
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()


@admin.route("/headreview",methods=["POST"])
def Headreview():
    if request.method =="POST":
        id = request.form["id"]
        status = request.form["status"]
        manageruser = request.form["manageruser"]
        nameaction = request.form["nameaction"]
        action = request.form["action"]
        remark = request.form["remark"]
        cancel = request.form["cancel"]
        actioncancel = request.form["actioncancel"]
        useremployeeID = request.form["user_employeeID"]
        user_name_lave = request.form["user_name_lave"]
        if cancel == '10':
            try:
                con.connect()
                cur = con.cursor()
                logsql = "insert into log_leave (log_lea_id,log_action,log_action_by,log_remark) VALUES(%s, %s,%s,%s)"
                cur.execute(logsql,(id,actioncancel,nameaction,remark))
                con.commit()

                sql = "UPDATE `db_leave` SET `lea_status`=%s WHERE `lea_id`=%s "
                cur.execute(sql,(cancel,id))
                con.commit()

                cur.execute(f"SELECT con_email FROM db_contact WHERE con_employee_ID = '{useremployeeID}' ")
                email = cur.fetchall()

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

                subject = 'รายงานผลการขอลางาน'
                msg = f"""
                        <html>
                            <head></head>
                            <body style="font-family:'Prompt', sans-serif;font-size:20px;color:#079992">
                                <h2>ขออนุญาตลางาน</h2>
                                <h3>เรียนคุณ {user_name_lave} </h3>
                                <h3>ไม่อนุญาติให้ลา เนื่องจาก {remark}</h3>
                                <hr style="color:#079992">
                                <h3>CES ADMIN</h3>
                                <a href="http://ceseservice.dyndns.org:88/" style="color:#079992" >CES-ESERVICE</a>
                            </body>
                        </html>

                            """
                emailto = email[0] #ข้อมูลที่ลูปมาเป็น type tuple เลยต้องดึงค่าออกมาก่อน
                sendthai(emailto[0],subject,msg)
        #-----------------------------------------------------------------------------------------------------------
                return redirect(url_for('admin.Leavereview'))
            except Exception as e:
                print(e)
            finally:
                print("Close")
                cur.close()
                con.close()
        if cancel != '10':
            try:
                con.connect()
                cur = con.cursor()

                logsql = "insert into log_leave (log_lea_id,log_action,log_action_by,log_remark) VALUES(%s, %s,%s,%s)"
                cur.execute(logsql,(id,action,nameaction,remark))
                con.commit()

                sql = "UPDATE `db_leave` SET `lea_status`=%s WHERE `lea_id`=%s "
                cur.execute(sql,(status,id))
                con.commit()
                if status == "1":
                    qemail = f"select con_email from db_contact where con_name = '{manageruser}' "
                    cur.execute(qemail)
                    email = cur.fetchall()
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

                    subject = 'ขออนุญาตลางาน'
                    msg = f"""
                                <html>

                                    <head></head>
                                    <body style="font-family:'Prompt', sans-serif;font-size:20px;color:#079992">
                                        <h2>ขออนุญาตลางาน</h2>
                                        <h3>เรียนคุณ {manageruser} </h3>
                                        <h3>มีพนักงานภายใต้การบังคับบัญชาของท่านขอลางาน รบกวนตรวจสอบเพื่อพิจารณาด้วยครับ</h3>
                                        <hr style="color:#079992">
                                        <h3>CES ADMIN</h3>
                                        <a href="http://ceseservice.dyndns.org:88/" style="color:#079992" >CES-ESERVICE</a>
                                    </body>
                                </html>

                            """
                    emailto = email[0] #ข้อมูลที่ลูปมาเป็น type tuple เลยต้องดึงค่าออกมาก่อน
                    sendthai(emailto[0],subject,msg)
        #-----------------------------------------------------------------------------------------------------------
                flash("Successfully")
                return redirect(url_for('admin.Leavereview'))
            except Exception as e:
                print(e)
            finally:
                print("Close")
                cur.close()
                con.close()


@admin.route("/hrreview",methods=["POST"])
def Hrreview():
    if request.method =="POST":
        id = request.form["id"]
        status = request.form["status"]
        leavenumd = request.form["leavenumd"]
        leavenumh = request.form["leavenumh"]
        employeeid = request.form["employeeid"]
        typeleave = request.form["typeleave"]
        nameaction = request.form["nameaction"]
        action = request.form["action"]
        remark = request.form["remark"]
        try:
            con.connect()
            cur = con.cursor()
            logsql = "insert into log_leave (log_lea_id,log_action,log_action_by,log_remark) VALUES(%s,%s,%s,%s)"
            cur.execute(logsql,(id,action,nameaction,remark))
            con.commit()

            sql = "UPDATE `db_leave` SET `lea_status`=%s WHERE `lea_id`=%s "
            cur.execute(sql,(status,id))
            con.commit()

            sql = f"SELECT * from db_contact WHERE con_employee_ID = '{employeeid}' "
            cur.execute(sql)
            leaveday = cur.fetchall()
            if typeleave == 'ลากิจ':
                myday = float(leaveday[0][8]) #ดึงค่าวันจาก database
                mydayH = float(leaveday[0][9]) #ดึงค่าชั่วโมงจาก database
                cal = (myday*8)+mydayH #แปลงเป็นหน่วยชั่วโมง
                leavenumd = float(leavenumd) #รับค่าจากผู้ใช้งานเป็นหน่วยวัน
                leavenumh = float(leavenumh) #รับค่าจากผู้ใช้งานเป็นหน่วยชั่วโมง
                cal1 = (leavenumd*8)+leavenumh
                calleave = cal - cal1
                if calleave >= 0:
                    sum = int(calleave//8) # วัน
                    a = (calleave/8)-sum
                    z = float(a*8) #ชั่วโมง
                else:
                    calleave=calleave*(-1)
                    sum = int(calleave//8) # วัน
                    a = (calleave/8)-sum
                    sum= sum*(-1)
                    z = float(a*8) #ชั่วโมง
                    z= z*(-1)
                sql = f'''UPDATE `db_contact` SET `prosonal_leave`='{sum}',prosonal_leave_h='{z}' WHERE `con_employee_ID`='{employeeid}' '''
                cur.execute(sql)
                con.commit()
            if typeleave == 'ลาพักร้อน':
                myday = float(leaveday[0][10])
                mydayH = float(leaveday[0][11])
                cal = (myday*8)+mydayH
                leavenumd = float(leavenumd)
                leavenumh = float(leavenumh)
                cal1 = (leavenumd*8)+leavenumh
                calleave = cal - cal1
                if calleave >= 0:
                    sum = int(calleave//8) # วัน
                    a = (calleave/8)-sum
                    z = float(a*8) #ชั่วโมง
                else:
                    calleave=calleave*(-1)
                    sum = int(calleave//8) # วัน
                    a = (calleave/8)-sum
                    sum= sum*(-1)
                    z = float(a*8) #ชั่วโมง
                    z= z*(-1)
                sql = f'''UPDATE `db_contact` SET `vacation_leave`='{sum}',vacation_leave_h='{z}' WHERE `con_employee_ID`='{employeeid}' '''
                cur.execute(sql)
                con.commit()
            if typeleave == 'ลาป่วย':
                myday = float(leaveday[0][12]) #ค่าจาก database หน่วยเป็น วัน
                mydayH = float(leaveday[0][13]) #ค่าจาก database หน่วยเป็น ชั่วโมง
                cal = (myday*8)+mydayH #แปลงค่าให้เป็นหน่วย ชั่วโมง
                leavenumd = float(leavenumd)#รับค่าจากผู้ใช้งานเป็นหน่วยวัน
                leavenumh = float(leavenumh)#รับค่รับค่าจากผู้ใช้งานเป็นหน่วยชั่วโมง
                cal1 = (leavenumd*8)+leavenumh
                calleave = cal - cal1
                if calleave >= 0:
                    sum = int(calleave//8) # วัน
                    a = (calleave/8)-sum
                    z = float(a*8) #ชั่วโมง
                else:
                    calleave=calleave*(-1)
                    sum = int(calleave//8) # วัน
                    a = (calleave/8)-sum
                    sum= sum*(-1)
                    z = float(a*8) #ชั่วโมง
                    z= z*(-1)
                sql = f'''UPDATE `db_contact` SET `sick_leave`='{sum}',sick_leave_h='{z}' WHERE `con_employee_ID`='{employeeid}' '''
                cur.execute(sql)
                con.commit()
            if typeleave == 'ลาอื่นๆ':
                myday = float(leaveday[0][14]) #ค่าจาก database หน่วยเป็น วัน
                mydayH = float(leaveday[0][15]) #ค่าจาก database หน่วยเป็น ชั่วโมง

                leavenumd = float(leavenumd) #รับค่าจากผู้ใช้งานเป็นหน่วยวัน
                leavenumh = float(leavenumh) #รับค่รับค่าจากผู้ใช้งานเป็นหน่วยชั่วโมง

                myday = leavenumd+myday
                mydayH = leavenumh+mydayH

                if mydayH == 8:
                    myday = myday+1
                    mydayH = 0
                if mydayH > 8:
                    myday = myday+1
                    mydayH = mydayH-8


                sum = int(myday) # วัน
                z = float(mydayH) #ชั่วโมง
                sql = f'''UPDATE `db_contact` SET `other_leave`='{sum}',other_leave_h='{z}' WHERE `con_employee_ID`='{employeeid}' '''
                cur.execute(sql)
                con.commit()
            flash("Successfully")
            return redirect(url_for('admin.Leavereview'))
        except Exception as e:
            print(e)
        finally:
            print("Close")
            cur.close()
            con.close()


@admin.route("/comments")
def Comments():
    if "username" not in session:
        return render_template("/login.html")
    return render_template("comments.html",part="comments",employee=noti.Employee(),notification=noti.Notification(),permissions=roles.Checkpermissions())


@admin.route("/sendcomment",methods=["POST"])
def Sendcomment():
    if request.method =="POST":
        name = request.form["name"]
        employeeid = request.form["employeeid"]
        subject = request.form["subject"]
        message = request.form["message"]
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
        try:
            con.connect()
            cur = con.cursor()
            sql = "insert into db_comments (comment_name,comment_employeeid,comment_subject,comment_comment,comment_file) VALUES(%s,%s,%s,%s,%s)"
            cur.execute(sql,(name,employeeid,subject,message,path))
            con.commit()
            flash("ขอบคุณสำหรับความคิดเห็นของท่าน")
            return redirect(url_for("admin.Profile"))
        except Exception as e:
            print (e)
        finally:
            print("Colse")
            cur.close()
            con.close()



@admin.route("/commentinbox")
def Commentinbox():
    if "username" not in session:
        return render_template("/login.html")
    permissions=roles.Checkpermissions()
    if permissions[0][7] != 1:
        return redirect(url_for('admin.Profile'))
    try:
        con.connect()
        cur = con.cursor()
        sql = f"select * from db_comments where comment_status < 2 order by comment_id desc"
        cur.execute(sql)
        comment = cur.fetchall()
        return render_template("commentinbox.html",part="commentinbox",comment = comment,scomment=len(comment),employee=noti.Employee(),notification=noti.Notification(),permissions=roles.Checkpermissions())
    except Exception as e:
        print (e)
    finally:
        print("Colse")
        cur.close()
        con.close()

@admin.route("/readcomment",methods=["POST"])
def Readcomment():
    if request.method == "POST":
        commentid = request.form["commentid"]
        comment_status = request.form["comment_status"]
    try:
        con.connect()
        cur = con.cursor()

        sql = "select * from db_comments where comment_id = %s"
        cur.execute(sql,(commentid))
        read = cur.fetchall()

        cur.execute(f"update db_comments set comment_status = '{comment_status}' where comment_id = '{commentid}' ")
        con.commit()

        return render_template("readcomment.html",part="commentinbox",read=read,employee=noti.Employee(),notification=noti.Notification(),permissions=roles.Checkpermissions())
    except Exception as e:
        print (e)
    finally:
        print("Colse")
        cur.close()
        con.close()


@admin.route("/deletecomment",methods=["POST"])
def Deletecomment():
    if request.method == "POST":
        commentid = request.form["commentid"]
        comment_status = request.form["comment_status"]
    try:
        con.connect()
        cur = con.cursor()

        cur.execute(f"update db_comments set comment_status = '{comment_status}' where comment_id = '{commentid}' ")
        con.commit()

        return redirect(url_for('admin.Commentinbox'))
    except Exception as e:
        print (e)
    finally:
        print("Colse")
        cur.close()
        con.close()


@admin.route("/trashcomment")
def Trashcomment():
    if "username" not in session:
        return render_template("/login.html")
    permissions=roles.Checkpermissions()
    if permissions[0][7] != 1:
        return redirect(url_for('admin.Profile'))

    try:
        con.connect()
        cur = con.cursor()
        sql = "select * from db_comments where comment_status = 2 order by comment_id desc"
        cur.execute(sql)
        trash = cur.fetchall()
        return render_template("trashcomment.html",part="commentinbox",trash=trash,strash=len(trash),employee=noti.Employee(),notification=noti.Notification(),permissions=roles.Checkpermissions())
    except Exception as e:
        print (e)
    finally:
        print("Colse")
        cur.close()
        con.close()


@admin.route("/readtrashcomment",methods=["POST"])
def Readtrashcomment():
    if request.method == "POST":
        commentid = request.form["commentid"]
    try:
        con.connect()
        cur = con.cursor()

        sql = "select * from db_comments where comment_id = %s"
        cur.execute(sql,(commentid))
        read = cur.fetchall()
        return render_template("readtrashcomment.html",part="commentinbox",read=read,employee=noti.Employee(),notification=noti.Notification(),permissions=roles.Checkpermissions())
    except Exception as e:
        print (e)
    finally:
        print("Colse")
        cur.close()
        con.close()



@admin.route("/deletetrash",methods=["POST"])
def Deletetrash():
    if request.method == "POST":
        commentid = request.form["commentid"]
    try:
        con.connect()
        cur = con.cursor()
        sql = "delete from db_comments where comment_id = %s"
        cur.execute(sql,(commentid))
        con.commit()
        flash("ทำรายการสำเร็จ")
        return redirect(url_for('admin.Trashcomment'))
    except Exception as e:
        print (e)
    finally:
        print("Close")
        cur.close()
        con.close()


@admin.route("/addholiday",methods=["POST"])
def Addholiday():
    if request.method == "POST":
        nameholiday = request.form['nameholiday']
        dateholiday = request.form['dateholiday']
    try:
        con.connect()
        cur = con.cursor()
        sql = "insert into holidays (name_holidays,date_holidays) VALUES(%s,%s)"
        cur.execute(sql,(nameholiday,dateholiday))
        con.commit()
        return redirect(url_for('scan.Checkmyscan'))
    except Exception as e:
        print (e)
    finally:
        print('Close')
        cur.close()
        con.close()
