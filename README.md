Amoki-Music
===========

External Requirements
---------------------
* Firefox

Install
---------
* `git clone git@github.com:Amoki/Amoki-Music.git` : retrieve the repo
* `cd Amoki-Music`
* `virtualenv --no-site-packages .v_env` : create a virtual-env for python code
* `source .v_env/bin/activate` : activate the v_env.
* `pip install https://www.djangoproject.com/download/1.7c1/tarball/` : install django 1.7
* `pip install -r requirements.txt` : install all requirements
* `./manage.py syncdb` : create DB
* `./manage.py migrate` : migrate DB


Configure
---------
#### Firefox :
```
In about:config set "browser.link.open_newwindow.override.external" to 1
```
It will open new url in the current tab

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

[Chrome :](https://chrome.google.com/webstore/detail/amoki-music/ieinfogigllinbiihpecpopcmkdopadm)

[Firefox :](https://addons.mozilla.org/fr/firefox/addon/amoki-music/)
