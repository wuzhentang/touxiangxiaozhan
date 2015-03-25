#! /usr/bin/env python
# coding:utf-8

"""
This module is use for generate page of user informations.
"""
import sys


__all__ = ["print_page_beg", "print_page_end", \
    "print_user_info_page", "print_test_page", "print_error_page"]


reload(sys).setdefaultencoding('utf8')

def print_page_beg(title):
    """"print html conent and title message. """
    print "Content-type: text/html"
    print
    print """
	<html xmlns="http://www.w3.org/1999/xhtml" xml:lang = "zh-cmn-Hans" lang = "zh-cmn-Hans">
	<head>
	<meta http-equiv = "Content-type" content = "text/html; charset = utf-8" />"""
    print "<title>%s</title>" % title
	

def print_page_end():
    """print the html tag of page end"""
    print """
		</body>
	</html>"""


def print_user_info_page(username, uid, email, image_name, register_time):
    """use for print user informations."""
    print """
	<style>
	*{margin:0 auto;padding:0 auto;}
	a{
		text-decoration:none;
	}
	a:hover{
		text-decoration:underline;
	}
	.logout{
		display:block;
		float:right;
		clear:both;
		width:80px;
		height:30px;
		text-align:center;
		background-color:#ddd;
		margin-top:10px;
		margin-right:20px;
		line-height:30px;
	}
	body{
		font-family: Arial, sans-serif; 
		font-size: 11p;
	}
	.boxs{
		border:1px solid #eee;
		margin:100px auto;
		width:700px;
		height:350px;
	}
	ul{
		list-style:none;
		margin-top:20px;
		margin-left:10px;
		padding:0;
		float:left;
	}
	ul label{
		display:inline-block;
		font-size:15px;
		padding:0;
		width:100px;
	}
	ul li{
		padding:0;
		margin:20px;
	}

	.submit-input{
		float:right;
		margin-top:20px;
	}
	.image_filepath{
		margin-right:10px;
		float:right;
		padding-top:20px;
		text-align:center;
	}
	.image_filepath input{
		display:block;
		margin-top:5px;
		margin-left:10px;
		margin-left:70px;
	}
	.imgs{
		border:1px solid #ddd;
		height:150px;
		width:150px;
		
	}
	.imgs img{
		width:100%;
		height:100%;
	}
	</style>
	</head>
	<body>"""
	
    print """<a href="/index.html" class="logout">退出</a><br/>"""
    print """<div class="boxs">
		    <div style="background-color:#E5E5E5;width:100%;text-align:center;font-size:30px;">用户信息</div>
            <form method="post" action="update_user_info.py" name="register_info" 
                enctype="multipart/form-data" onsubmit="return is_modify();">"""
    print """<ul>"""
    print """ <input type = "hidden" value = %s name="uid">""" % uid
    print "<li><label>用户名:</label><label>%s</label></li>" % username
    print "<li><label>UID:</label><label>%s</label></li>" % uid
    print "<li><label>Email:</label><label>%s</label></li>" % email
    print "<li><label>注册时间:</label>%s</li>" % register_time
    print """<li class="submit-input" style='float:right;'>
	        <input type="submit" value="提交修改" 
			    style="width:80px;height:30px;"/></li>"""
    
    print "</ul>"
    print """<div class="image_filepath">"""

    print """	<div class="imgs" id="preview">
	            <img src="/pic/%s"/></div>""" % image_name

    print """
	    <a onClick="updateImg();" style="cursor:pointer;display:block;margin-top:10px;height:30px;width:80px;border:1px solid #eee;background-color:#e5e5e5;text-align:center;line-height:30px;">修改头像</a>
		<div style="display:none;"><input type="file" name="image" id="fileName" width="5" style="" value='修改头像' onchange="handleFiles(this.files)"/></div>
				
			</div>
		</form>
	</div>""" 

    print """<div id="filecontent"></div>"""

    print """<script type="text/javascript">
		function handleFiles(files){
			for (var i = 0; i < files.length; i++) {
				var file = files[i];
				var imageType = /image.*/;
				
				if (!file.type.match(imageType)) {
					alert("上传文件不是图片，请上传图片!");
					continue;
				}
				if(!file.type.match("image/jpeg")){
					alert("上传文件格式不是jpg图片，请图片类型!");
					continue;
				}
				
				var preview = document.getElementById("preview");
				preview.innerHTML = "";
				var img = document.createElement("img");
				img.classList.add("obj");
				img.file = file;
				preview.appendChild(img);
				
				var reader = new FileReader();
				reader.onload = (function(aImg){
					return function(e){
						aImg.src = e.target.result;
					};
				})(img);
				reader.readAsDataURL(file);
			}
		}
		function updateImg(){
			var file = document.getElementById("fileName");
			file.click();
		}
		
		function is_modify(){
			var file=document.getElementById("fileName");
			if(file.value==""){
				alert("未做任何修改");
				return false;
			}
			return true;
		}
	</script>
	"""


def print_error_page(error_message, go_back_url):
    """print error message in page"""
    print """
	<style>
		*{margin:0 auto;padding:0 auto;}
		.boxs{
			border:1px solid #eee;
			margin:100px auto;
			width:400px;
			height:200px;
			padding:20px 20px;
	}
	.go-back{
		display:block;
		border:1px solid #eee;
		background-color:#ccc;
		height:40px;
		width:80px;
		font-size:30px;
		line-height:40px;
		text-align:center;
		text-decoration:none;
		color:black;
		margin-top:70px;
	}
	</style>
	</head>
	<body>
	<div class="boxs">"""
	
	
    print """<div style = "font-size: 26px; font-weight: bold;
	        margin-bottom:10px;text-align:center;">%s</div>""" % error_message
    print """<a href=%s class="go-back">返回</a>
	</div>""" % go_back_url
	

def print_test_page(test_messge):
    """use for print test page"""
    print_page_beg("test_page")
    print """
		</head>
		<body>
		    <div style = "font-size: 26px; font-weight: bold;
			    margin-bottom:10px;">%s</div>""" % test_messge
    print_page_end()
	
	
	

