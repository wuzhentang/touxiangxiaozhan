#! /usr/bin/env python
# coding:utf-8


"""
This module is used to process user information update.
"""

import cgi
import os

from page_gen import *
from database import get_user_info


def update_user_info():
	update_info=cgi.FieldStorage()
	
	try:
		image=update_info["image"]
		image_data=image.file.read()
		image_filename=image.filename
		uid=update_info["uid"].value
	except KeyError:
		print_page_beg("修改失败")
		print_error_page("无法获取修改信息！","/register.html")
		print_page_end()
	else:
		user_info=get_user_info("UID",uid)
		if image_filename!="":			
			image_filename=user_info["picture_name"]
			image_file=open("../pic/"+image_filename,'wb')			
			try:	
				image_file.write(image_data)
			finally:				
				image_file.close()
			
		print_page_beg("修改成功")
		print_user_info_page(user_info["username"],user_info["uid"],user_info["email"],\
				user_info["picture_name"],user_info["register_time"])
		print_page_end()
	
#print_test_page("这里是修改提交页面   未完待续……")
update_user_info()