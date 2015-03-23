#! /usr/bin/env python
# coding:utf-8

"""
This module is process register event,if informations of user is valid,
 a new record of the user will be inserted into mysql server
 else print error page.

"""
import cgi
import re
import os

from page_gen import print_page_beg
from page_gen import print_page_end
from page_gen import print_user_info_page
from page_gen import print_test_page
from page_gen import print_error_page
from database import  get_user_info,add_new_user


def validate_email(email):

    if len(email) > 7:
        if re.match("^[0-9a-z][_.0-9a-z-]{0,31}@([0-9a-z][0-9a-z-]{0,30}[0-9a-z]\.){1,4}[a-z]{2,4}$", email) != None:
            return True
    return False
	
def validate_username(username):
	if re.match("^\w{4,20}$", username) != None:
		return True
	return False


def check_register_info(username,email,password1,password2):
	if not (username and  email and password1  and password2):
		return False,"注册信息不完整 :( "
	if not validate_email(email):
		return False,"email地址无效 :( "
	if not validate_username(username):
		return False,"用户名格式不正确 :( "
		
	if  username=="default" or get_user_info("用户名",username):
		return False,"用户名已存在 :( "
	if  get_user_info("email",email):
		return False,"email 已注册 :(  "
	if password1!=password2:
		return False,"两次输入密码不一致!"
	return True,""
		
def register():
	register_info=cgi.FieldStorage()
	username=""
	email=""
	password1=""
	password2=""
	image_filename=""
	image_data=None
	
	try:
		username=register_info["username"].value
		email=register_info["email"].value
		password1=register_info["password"].value
		password2=register_info["sec_password"].value
		image=register_info["image"]
		image_data=image.file.read()
		image_filename=image.filename
	except KeyError:
		print_page_beg("注册失败")
		print_error_page("注册信息不完整！","/register.html")
		print_page_end()
	else:
		is_valid,message=check_register_info(username,email,password1,password2)
		if  is_valid:
			if image_filename=="": #use default avatar 
#				image_filename=username+".jpg"
				image_filename=username
				os.system("cp ../pic/default.jpg ../pic/"+image_filename)
			else:
#				image_filename=username+".jpg"
				image_filename=username
				image_file=open("../pic/"+image_filename,'wb')			
				try:	
					image_file.write(image_data)
				finally:				
					image_file.close()
			add_new_user(username,password1,email,image_filename)
			user_info=get_user_info("email",email)
			
			print_page_beg("注册成功")
			print_user_info_page(user_info["username"],user_info["uid"],user_info["email"],\
				user_info["picture_name"],user_info["register_time"])
		else:
			print_page_beg("注册失败")
			print_error_page(message,"/register.html")
		print_page_end()
		

#print_test_page("这里是注册提交页面  未完待续……")
register()