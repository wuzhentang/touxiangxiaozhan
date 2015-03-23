#! /usr/bin/env python
# coding:utf-8

"""
This module is process login event,if username name and password is legal print the user informations,
else print error page

"""

import cgi
import sys

from database import  get_user_info
from page_gen import *

	
def check_login(login_type,username,password):
	user_info=get_user_info(login_type,username)
	
	if user_info and user_info["password"]==password:
		return True,user_info
	else:
		return False,{}

	
def login():
	login_info=cgi.FieldStorage()
	login_type=""
	username=""
	password=""
	try:
		login_type=login_info["loginname"].value
		username=login_info["username"].value
		password=login_info["password"].value
	except KeyError:
		print_page_beg("登陆失败")
		print_error_page("用户名或密码错误！ :(","/index.html")
		print_page_end()
	else:	
		is_valid_user,user_info=check_login(login_type,username,password)
		if  is_valid_user:
			print_page_beg("登陆成功")
			print_user_info_page(user_info["username"],user_info["uid"],user_info["email"],\
				user_info["picture_name"],user_info["register_time"])
		else:
			print_page_beg("登陆失败")
			print_error_page("用户名或密码错误！ :(","/index.html")
		
		print_page_end()
		
#print_test_page()
login()

	    
