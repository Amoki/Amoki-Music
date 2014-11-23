Amoki-Music
===========

External Requirements
---------------------
* libevent
On ubuntu: `apt-get install libevent-dev`


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
#### Start the server 
```bash
pyhton manage.py runserver <ip:port>
```
Connect to your server and let you be guided by our awesome UI


Remotes
-------
You can download [Chrome](https://chrome.google.com/webstore/detail/amoki-music/ieinfogigllinbiihpecpopcmkdopadm) and [Firefox](https://addons.mozilla.org/fr/firefox/addon/amoki-music/) extensions to add musics to the server directly from Youtube !
