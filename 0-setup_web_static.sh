#!/usr/bin/env bash
#install Nginx if not installed
if [[ "$(which nginx | grep -c nginx)" == '0' ]]; then
	apt-get -y update
	apt-get -y install nginx
fi
HTML_HOME_PAGE="<!DOCTYPE html>
<html lang='en-us'>
	<head>
		<title>Web static deploy</title>
	</head>
	<body>
		<h1>My first web deployment</h1>
	</body>
</html>"
#create /data/ folder if not exist
mkdir /data/
#create /data/web_static/ if not exist
mkdir -p /data/web_static/
#Create /data/web_static/releases/ if not exist
mkdir -p /data/web_static/releases/
#Create /data/web_static/shared/ if not exist
mkdir -p /data/web_static/shared/
#Create /data/web_static/shared/ if not exist
mkdir -p /data/web_static/releases/test/
#create  a fake html file /data/web_static/release/test/index.html if not exist
echo "$HTML_HOME_PAGE" | sudo tee /data/web_static/releases/test/index.html > /dev/null
#Create a symbolic link /data/web_static/current linked to the /data/web_static/releases/test/ folder.
[ -d /data/web_static/current ] && rm -rf /data/web_static/current
ln -s /data/web_static/releases/test/ /data/web_static/current
#Give ownership of /data/ folder to the ubuntu User
chown -R ubuntu:ubuntu /data
sed -i '/# pass PHP scripts to FastCGI server/a location /hbnb_static/ { alias /data/web_static/current/; autoindex off; }' /etc/nginx/sites-available/default
service nginx restart
