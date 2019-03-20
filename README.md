# Amoki-Music

## External Requirements
```sh
sudo apt install redis-server python3.7 python3.7-dev
```

## Install
* `git clone git@github.com:Amoki/Amoki-Music.git` : retrieve the repo
* `cd Amoki-Music`
* `sudo pip3 install pipenv` : create a virtual-env for python code
* `pipenv install` : install all requirements


## Configure

#### env:
Create a file named youtube_key.json at the root folder with your youtube API key

## How to use

### In development

#### Activate the virtual_env
`pipenv shell`

#### Migrate DB
`./manage.py migrate`

#### Create admin account
`./manage.py createsuperuser`

#### Start the server
```bash
python manage.py runserver <ip:port>
```
Connect to your server and let you be guided by our awesome UI

#### See the swagger doc
http://locahost:8000/doc
