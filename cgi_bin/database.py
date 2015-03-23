#! /usr/bin/env python
# coding:utf-8

"""
This module provide API about mysql for other modules. 
"""

import sys
import time
import datetime
import os

import MySQLdb

__all__=["CHARSET","DATABASE_NAME","TABLE_NAME","get_user_info","add_new_user","update_user_image"]



CHARSET='utf8'
DATABASE_NAME="touxiangxiaozhan"
TABLE_NAME="user_info"

def connect_db():
	conf=open("../conf/website_db.conf","r")
	args={}
	try:
		for line in conf:
			line = line.split("=")
			args[line[0].strip()]=line[1].strip()
	finally:
		conf.close()
		
	try:
		conn=MySQLdb.connect(\
					host=args["mysql_host"],\
					port=int(args["mysql_port"]),\
					user=args["mysql_username"],\
					passwd=args["mysql_password"],\
					charset=CHARSET,\
				)
	except MySQLdb.Error,e:
		sys.stderr.write("Unable to connect to database %s: %d, %s" % (DATABASE_NAME,e.args[0], e.args[1]))
	else:
		return conn


def get_user_info(login_type,login_name):
	if login_type=="用户名":
		login_type="username"
	query_sql='SELECT * FROM '+TABLE_NAME+' where '+"`"+login_type+"`"+'='+'"'+login_name+'"'
	
	conn=connect_db()
	conn.select_db(DATABASE_NAME)
	cur=conn.cursor()
	count=cur.execute(query_sql)
	user_info={}
	if count>0:
		result=cur.fetchone()
		user_info["uid"]=result[0]
		user_info["username"]=result[1]
		user_info["password"]=result[2]
		user_info["email"]=result[3]
		user_info["picture_name"]=result[4]
		user_info["register_time"]=result[5]
	cur.close()
	conn.close()
	return user_info
	
def add_new_user(username,password,email,pic_file_name):
	register_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
	insert_sql="INSERT INTO "+TABLE_NAME+"(username,password,email,picture_name,register_time) \
				VALUES(%s,%s,%s,%s,%s)"
	
	conn=connect_db()
	conn.select_db(DATABASE_NAME)
	cur=conn.cursor()
	cur.execute(insert_sql,(username,password,email,pic_file_name,register_time))
	conn.commit()
	cur.close()
	conn.close()
	
def update_user_image(uid,new_file_name):
	conn=connect_db()
	conn.select_db(DATABASE_NAME)
	cur=conn.cursor()
	update_sql="UPDATE "+TABLE_NAME+" SET picture_name="+'"'+new_file_name+'"'+" WHERE UID = "+'"'+uid+'"'
	cur.execute(update_sql)
	conn.commit()
	cur.close()
	conn.close()

if __name__=="__main__":

#	add_new_user("wuzhentang","wugege","wuzhentangwu@163.com","default.jpb")
#	add_new_user("lian","lqp","unknow@qq.com","default.jpg")
	result=get_user_info("email","wuzhentangwu@163.com")
	print result
	
	result=get_user_info("username","lian")
	print result
	
	update_user_image("1","default.jpg")
	result=get_user_info("email","wuzhentangwu@163.com")
	print result;

	