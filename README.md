#1. apache服务器安装与配置
##1.1 apache安装
	apt-get install build-essential --fix-missing
	apt-get install apache2
		
##1.2 增加apache监听端口 9000
修改apache安装目录下的ports.cnf，一般为 /etc/apache2/目录下		
  

      NameVirtualHost *:80
      Listen 80
后增加一下两行：

    NameVirtualHost *:9000
    Listen 9000	
	   		
##1.3 给apache增加配置文件
###1.3.1 新建配置文件
在安装目录下的sites-available子目录，一般为：/etc/apache2/sites-available 新建一个配置文件

    vim touxiangxiaozhan

写入以下内容：
		

    <VirtualHost *:9000>
    	ServerAdmin webmaster@localhost
    	DocumentRoot /home/wzt/apacheWorkDir/touxiangxiaozhan
    	<Directory />
	    	Options FollowSymLinks
    		AllowOverride None
    	</Directory>
    	<Directory /home/wzt/apacheWorkDir/touxiangxiaozhan>
	    	Options Indexes FollowSymLinks MultiViews
    		AllowOverride None
    		Order allow,deny
    		allow from all
    	</Directory>
    
    #	ScriptAlias /cgi-bin/ /usr/lib/cgi-bin/
    	<Directory "/home/wzt/apacheWorkDir/touxiangxiaozhan/cgi_bin">
	    	AllowOverride None
    		Options +ExecCGI -MultiViews +SymLinksIfOwnerMatch
    		AddHandler cgi-script .cgi .py
    		Order allow,deny
    		Allow from all
    	</Directory>
    	DirectoryIndex index.py index.html default.py  default.html
    	ErrorLog ${APACHE_LOG_DIR}/error.log
    
    # Possible values include: debug, info, notice, warn, error, crit,
    # alert, emerg.
    LogLevel warn
    
    CustomLog ${APACHE_LOG_DIR}/access.log combined
    </VirtualHost>	
并将DocumentRoot、两个Directory后的/home/wzt/apacheWorkDir/touxiangxiaozhan换为站点所在的 根目录。注意第二个Directory的路径应为:"站点根目录/cgi_bin"。
		
###1.3.2 将新建配置加入apache中
进入安装目录下的sites-enabled子目录，一般为/etc/apache2/sites-enabled建立软连接到刚才所建文件，如 

    ln -s /etc/apache2/sites-available/touxiangxiaozhan ./touxiangxiaozhan
		
###1.3.3 让apache加载cgi处理模块
进入apache安装目录的mods-enabled，一般为/etc/apache2/mods-enabled/建一个软连接，连接到到安装目录下的mods-available子目录的cgi.load模块。如下：
				
    cd /etc/apache2/mods-enabled/
    ln -s ../mods-available/cgi.load
	
##1.4 重启apache服务器
	
    service apache2 restart
	
#2.安装及设计说明

##2.1 安装说明
	
###2.1.1 数据库初始化
			
进入站点根目录下的setup子目录，执行如下命令：

    mysql -h localhost -u root -p < ./init_database.sql 
该脚本创建名为touxiangxiaozhan的数据库并和user_info的表。并将该数据库的所有权限赋予用户名为：wuzhentang 密码为：wzt的用户。如果要修改mysql服务器的地址、端口号及新建的用户名和密码，在修改该.sql文件的同时要修改conf子目录的website_db.conf里的mysql_host、mysql_port、mysql_username，mysql_password对应的值。在配置文件中mysql服务器使用默认的3306端口号。
			
###2.1.2 安装python及mysql-python依赖
		
####2.1.2.1安装python：
    sudo apt-get install python
				
####2.1.2.2 安装mysql-python依赖
		
如果未安装pip，则先安装：

    easy_install pip
接着用pip安装mysql-python

    python -m pip install mysql-python

		
###2.1.3 站点代码获取及目录说明
		
####2.1.3.1代码获取
当前用户主目录下新建一个文件夹，并进入该文件夹后执行：

    git clone https://github.com/wuzhentang/touxiangxiaozhan.git
确保该文件夹及其所有父文件夹的的权限都至少为755。
			
####2.1.3.2 目录结构说明
在touxiangxiaozhan目录下，共包含index.html和register.html两个文件和cgi_bin、conf、pic、setup四个文件夹。其中:
#####a）index.html
站点主页面也为登录页面。
#####b) register.html
注册页面。
#####c) cgi_bin目录
存放网站要运行的cgi脚本。
######d）conf目录
站点配置文件夹，website_db.conf,包含连接数据库的参数。
#####e) pic目录
存储站点用户头像图片文件。
#####f)setup目录
存放站点初次安装时使用的脚本或文件。目前只包含init_database.sql文件，用于创建数据和表。
		
###2.1.4 修改pic目录的访问权限,使得apache有权限在该文件夹添加和修改文件。
在站点根目录执行	

    chmod 777 ./pic
		
###2.1.5 站点访问说明
由于本站点不是使用默认的80端口号，而是前文所设的8080，因此访问方式为：

    站点地址:9000
   在本机访问则为:

    http://localhost:9000 或
    http://127.0.0.1:9000
			
	
##2.2 设计说明
###2.2.1 整体设计
站点设计只包含要求的基本功能，包括：注册、登录、退出、头像修改和头像访问API。整个站点主要由三个页面组成，分别是：登陆页面、注册页面和用户信息显示页面。其中登陆页面为主页面，当用户已有账号时，可从主页面直接登录，登录成功后进入用户信息显示页面。如果用户是还未在本站注册的新用户，则从通过主页面的超链接跳转到用户注册页面，进行用户注册。注册成功后进入用户信息显示页面，在该页面可以修改自己的头像。
			
			    流程如下：
					
								登录页面(主页面)
								 /    \
						  已有账号/     \ 新用户
								/      \
						用已有账号登录       跳转到注册页面
							 /    \           	   /   \						 
						失败/      \成功    注册成功/     \注册失败
					      /        \            /       \
                显示出错信息       显示用户信息页面      显示失败原因
		   (可返回登录页面)          (此处可修改头像，        (可返回注册界面)
									   或者退出登录）
									   
									   
###2.2.2 数据库表设计及相关操作
		
####2.2.2.1表设计
数据库中只包含一张名为user_info的用户信息表。表中包含6个字段，名称和类型分别为：
						

    UID INT UNSIGNED NOT NULL AUTO_INCREMENT,\
    username 		varchar(30)
    password 		char(32)
    email 			varchar(50)
    picture_name 	varchar(50)
    register_time 	datetime
其中UID为主键，并为email和username建立索引，存储引擎为InnoDB，字符集为utf-8。
			
####2.2.2.2 数据库操作(database.py)
数据相关的操作在database模块完成，共提供三个接口：get_user_info、add_new_user、update_user_image。
			
#####a) get_user_info： get_user_info(login_type,login_name)
	功能：从数据库读取用户信息。
	参数含义：
		login_type：用户名、email或UID。
		login_name:即为登录类型对应的值。
	返回值：若存在，则返回用户信息的dict，否则返回一个空字典即{}。
					
#####b)add_new_user：add_new_user(username,password,email,pic_file_name)
	功能：添加新用户。
	参数含义：
		username：用户填写的用户名。
		password：用户密码。
		email：注册email。
		pic_file_name:在pic目录下，该用户的头像文件名称。
	返回值：无。
					
#####c) update_user_image：update_user_image(uid,new_file_name)
	功能：更新用户的头像文件名称。(暂未使用)
	参数含义：
		uid：用户的UID。
		new_file_name：新头像的文件在pic目录的名称。
	返回值：无。
			
			
		
###2.2.3 登录设计
 登录页面为主页面，登录方式有三种方案，分别是用户名、email和UID。其中用户名和email为用户注册时填写的信息，UID为注册成功时，系统自动生成。登录功能由index.html和login.py两部分组成。
index.html获取用户输入的信息，post到服务器交给login.py 脚本处理。
			
####2.2.3.1 login模块
login模块根据登录名称，从数据库读取用户信息，校验是否存在该用户名或者登录密码是否正确。如果正确则输出用户信息页面返回给客户端。login模块由check_login、login两个函数组成。
			
#####a) check_login：check_login(login_type,username,password)
	功能：校验用户名或密码是否有效。
	参数：
		login_type：用户名、email或UID。
		username：登录的名称。
		password：用户登入输入的密码。
	返回值：二元组。分别为指示用户是否登录成功的布尔值和包含用户信息的dict。
				
#####b)login:login()
	功能：取出表单数据，根据校验结果，返回给出错信息或者用户信息页面给客户端。
	参数：无。
	返回值：无。
				
				
###2.2.3 注册设计
注册功能由register.html和register.py两部分共同完成。register.py接收从register.html post到服务器注册信息。register.py模块校验注册信息的有效性，如果注册信息有效，则返回注册成功的用户信息页面，如果注册失败，返回出错信息。注册时用户可以选择自己上传图片或者直接采用默认图片作为头像。用户名只能由字母数字或下划线的4~20字符组成。
			
####2.2.3.1 register.py模块
register.py包含validate_email、check_register_info、register三个函数。
			  
######a) validate_email:validate_email(email)
	功能：校验用户输入的email地址是否有效。
	参数：
		email：用户注册填写的email地址。
	返回值：如果合法就返回True，否则返回False。
	
#####b)check_register_info:check_register_info(username,email,password1,password2)
	功能：检查注册信息的有效性，检索数据，查看用户名是否已经存在，email地址是否已经注册过及 两次输入密码是否一致。
	参数：
		username：注册填写的用户名。
		email：注册填写的email地址。
		password1：第一次输入的密码。
		password2：第二次输入的密码。
	返回值：注册信息合法则返回True，否则返回False。
					
#####c)register：register()

    功能：取出表单的注册数据，根据校验结果，输出注册失败页面或者注册成功的用 户信息页面并将新用户信息添加到数据库。
     参数：无。
    返回值：无。
			  
###2.2.4 头像修改
头像修改功能集成在用户信息显示页面，用户显示页面由page_gen模块生成，头像修改功能由update_user_info完成。update_user_info接收page_gen生成页面post过来的表单数据，包括UID和用户修改的头像数据。
			
####2.2.4.1 page_gen模块
该模块提供页面信息生成API，以供其他模块调用。包括以下几个函数：print_page_beg、print_page_end、print_user_info_page、print_test_page、print_error_page。
			
#####a) print_page_beg:print_page_beg(title)
	功能：输出html文档的头部信息。
	参数：
		title:html的标题信息。
	返回值：无。
				
#####b) print_page_end:print_page_end()
	功能：输出文档尾部信息。
	参数：无。
	返回值：无
#####c)print_user_info_page:print_user_info_page(username,uid,email,image_name,register_time)
	功能：输出用户信息的html的中部信息。
	参数：
		username：用户名。
		uid：用户的UID。
		email：注册时填写的email地址。
		image_name：头像文件的文件名称。
		register_time：用户的注册时间。
	返回值：无。
			
#####d) print_test_page:print_error_page(error_message,go_back_url)
	功能：输出出错信息。
	参数：
		error_message:要输出的出错消息。
		go_back_url:回退页面地址。
	返回值：无。
			
#####e) print_test_page:print_test_page(test_messge)
	功能：打印测试页面，调试时使用。
	参数：
		test_messge:要输出的测试消息。
	返回值：无。
		

####2.2.4.2 update_user_info模块
update_user_info模块为用户修改头像信息时调用。当用户在用户信息页面修改完头像，	post到服务器后，服务器将新头像文件替换就头像文件。该模块较为简单，只包含一个：update_user_info函数。
			
#####a)update_user_info:update_user_info()
	功能：修改用户头像文件。
	参数：无。
	返回值：无。
				
				
			
###2.2.5 头像访问API
由于用户名称具有唯一性，因此直接采用用户名称作为用户的头像的文件名，存储于pic的目录下，头像访问API如下例：
				

    username = "xyz"
    url = "http://www.touxiangxiaozhan.com/pic/"+username
				
		
###2.2.6 登出
通过超链接页面直接跳转到登入的主页面。
				
			
			
			
			