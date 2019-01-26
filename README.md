Amoki-Music
===========
External Requirements
---------------------
```sh
sudo apt install redis-server
```


Install
---------
* `git clone git@github.com:Amoki/Amoki-Music.git` : retrieve the repo
* `cd Amoki-Music`
* `pip3 install pipenv` : create a virtual-env for python code
* `pipenv shell` : activate the virtual_env
* `pipenv install` : install all requirements
* `./manage.py migrate` : migrate DB
* `./manage.py createsuperuser` : add your own admin.


Configure
---------

#### env:
Create a file named youtube_key.json at the root folder with your youtube key

How to use
----------
## In development
#### Start the server
```bash
python manage.py runserver <ip:port>
```
Connect to your server and let you be guided by our awesome UI
