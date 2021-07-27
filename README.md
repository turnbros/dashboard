# Flask Dashboard

## Getting Started
### Setup the virtual environment
```shell
flask-dashboard % virtualenv venv
flask-dashboard % source venv/bin/activate
(venv) flask-dashboard % pip install -r requirements.txt
```
### Configure the dashboard
```editorconfig
[site]
title = Flask Dashboard
name_1 = Flask
name_2 = Dashboard
bind_ip = 0.0.0.0
bind_port = 8443
session_type = filesystem
secret_key = foobarbaz123456

[auth]
client_id = 123456bazbarfoo
client_secret = foo123bar456baz
api_base_url = https://foo.us.auth0.com
access_token_url = https://foo.us.auth0.com/oauth/token
authorize_url = https://foo.us.auth0.com/authorize
callback_url = http://127.0.0.1:8443/callback
logout_redirect_url = https://foo.app/
groups_claim = https://foo.app/claims/groups
```

### Start the Dashboard
```shell
(venv) flask-dashboard % python app.py
```

### Explore the dashboard
![Dashboard Screenshot](docs/images/sample_dashboard.png?raw=true "Dashboard Screenshot")
