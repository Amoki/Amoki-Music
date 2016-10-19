Amoki-Music
===========
[![Circle CI](https://circleci.com/gh/Amoki/Amoki-Music.svg?style=svg)](https://circleci.com/gh/Amoki/Amoki-Music)[![Coverage Status](https://coveralls.io/repos/Amoki/Amoki-Music/badge.svg?branch=endpoints-tests&service=github)](https://coveralls.io/github/Amoki/Amoki-Music?branch=master)
External Requirements
---------------------
* libevent
	* On ubuntu :
	```
	apt-get install redis-server
	sudo apt-get install libpcre3 libpcre3-dev
	```


Install
---------
* `git clone git@github.com:Amoki/Amoki-Music.git` : retrieve the repo
* `cd Amoki-Music`
* `virtualenv -p python3 --no-site-packages .v_env` : create a virtual-env for python code
* `source .v_env/bin/activate` : activate the v_env
* `pip install -r requirements.txt` : install all requirements
* `./manage.py migrate` : migrate DB
* `./manage.py createsuperuser` : add your own admin.


Configure
---------

#### env:
```bash
export YOUTUBE_KEY="your Youtube API key"
export SOUNDCLOUD_KEY="your Soundcloud API key"
```
or
```bash
SET YOUTUBE_KEY="your youtube API key"
SET SOUNDCLOUD_KEY="your Soundcloud API key"
```

How to use
----------
## In development
#### Start the server
```bash
python manage.py runserver <ip:port>
```
Connect to your server and let you be guided by our awesome UI

## In production
#### configure nginx
```
location / {
    include /etc/nginx/uwsgi_params;
    uwsgi_pass unix:/path/to/django.socket;
}

location /ws/ {
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_pass http://unix:/path/to/web.socket;
}
```

#### Update production
```bash
git pull origin master
python manage.py collectstatic
yes
python manage.py migrate
```

#### Start uwsgi
```bash
uwsgi --virtualenv /path/to/virtualenv --socket /path/to/django.socket --buffer-size=32768 --workers=5 --master --module wsgi_django
uwsgi --virtualenv /path/to/virtualenv --http-socket /path/to/web.socket --gevent 1000 --http-websockets --workers=2 --master --module wsgi_websocket
```

