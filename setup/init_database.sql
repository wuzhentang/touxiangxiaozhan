
CREATE DATABASE IF NOT EXISTS touxiangxiaozhan default character set utf8 COLLATE utf8_general_ci;
GRANT ALL PRIVILEGES  ON touxiangxiaozhan.* TO wuzhentang@localhost IDENTIFIED  BY 'wzt';
flush privileges;
USE touxiangxiaozhan;
CREATE TABLE IF NOT EXISTS user_info(
						UID INT UNSIGNED NOT NULL AUTO_INCREMENT,
						username varchar(30),
						password char(32),
						email varchar(50),
						picture_name varchar(50),
						register_time datetime,
						PRIMARY KEY(UID),
						UNIQUE INDEX EmailIndex(email),
						UNIQUE INDEX UsernameIndex(username)
						) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SHOW CREATE DATABASE touxiangxiaozhan \G						
SHOW CREATE TABLE user_info \G