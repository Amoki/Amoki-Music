Amoki-Music
===========

External Requirements
---------------------
* libevent
On ubuntu: `apt-get install libevent-dev`
On ubuntu: `apt-get install redis-server`
On ubuntu: `sudo apt-get install libpcre3 libpcre3-dev`


Install
---------
* `git clone git@github.com:Amoki/Amoki-Music.git` : retrieve the repo
* `cd Amoki-Music`
* `virtualenv --no-site-packages .v_env` : create a virtual-env for python code
* `source .v_env/bin/activate` : activate the v_env
* `pip install -r requirements.txt` : install all requirements
* `./manage.py syncdb` : create DB
* `./manage.py migrate` : migrate DB



Configure
---------

#### env:
```bash
export YOUTUBE_KEY="your youtube API key"
```
or
```bash
SET YOUTUBE_KEY="your youtube API key"
```

How to use
----------
## In development
#### Start the server 
```bash
pyhton manage.py runserver <ip:port>
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
ggpull
pyhton manage.py collectstatic
yes
python manage.py migrate
```

#### Start uwsgi
```bash
uwsgi --virtualenv /path/to/virtualenv --socket /path/to/django.socket --buffer-size=32768 --workers=5 --master --module wsgi_django
uwsgi --virtualenv /path/to/virtualenv --http-socket /path/to/web.socket --gevent 1000 --http-websockets --workers=2 --master --module wsgi_websocket
```

