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
        check = request.form["check"]
        reviewleave = request.form["reviewleave"]
        approveleave = request.form['approveleave']
        write_post = request.form['write_post']
