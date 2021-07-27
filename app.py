import logging
import config_handler
from flask import Flask
from flask import request
from flask import session
from flask import redirect
from functools import wraps
from modules import ModuleHandler
from auth_handler import AuthHandler
from six.moves.urllib.parse import urlencode


app = Flask(__name__)


################
## Auth Stuff ##
################
@app.route('/login')
def login():
    return auth_handler.auth0.authorize_redirect(redirect_uri=config.get_string_value("auth", "callback_url"))


@app.route('/logout')
def logout():
    session.clear()
    params = {'returnTo': config.get_string_value("auth", "logout_redirect_url"), 'client_id': config.get_string_value("auth", "client_id")}
    return redirect(f"{config.get_string_value('auth', 'api_base_url')}/v2/logout?{urlencode(params)}")


@app.route('/callback')
def callback_handling():
  # Handles response from token endpoint
  auth_handler.auth0.authorize_access_token()
  resp = auth_handler.auth0.get('userinfo')
  userinfo = resp.json()

  # Store the user information in flask session.
  session['jwt_payload'] = userinfo
  session['profile'] = {
    'user_id': userinfo['sub'],
    'given_name': userinfo['given_name'],
    'family_name': userinfo['family_name'],
    'name': userinfo['name'],
    'nickname': userinfo['nickname'],
    'picture': userinfo['picture'],
    'email': userinfo['email'],
    'groups': userinfo[config.get_string_value("auth", "groups_claim")]
  }
  return redirect('/')


def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if 'profile' not in session:
      return redirect('/login')
    return f(*args, **kwargs)
  return decorated


################
## Site Stuff ##
################
@app.route('/', methods=['GET', ])
@app.route('/<module_name>', methods=['GET', 'POST'])
@requires_auth
def request_module(module_name=None):
    response = module_handler.render_module(module_name, session['profile'], data=request.data, form_data=request.form)
    if response is None:
        return "Module Not Found!", 404
    return response


@app.route('/modules/<module_name>/styles/<style_file>', methods=['GET'])
@requires_auth
def request_module_style(module_name=None, style_file=None):
    response = module_handler.site_modules.get(module_name).get_module_style(style_file)
    if response is None:
        return "Module Not Found!", 404
    return response


@app.route('/modules/<module_name>/scripts/<script_file>', methods=['GET'])
@requires_auth
def request_module_script(module_name=None, script_file=None):
    response = module_handler.site_modules.get(module_name).get_module_script(script_file)
    if response is None:
        return "Module Not Found!", 404
    return response


if __name__ == "__main__":
  logging.info("Loading auth handler...")
  auth_handler = AuthHandler(app)

  logging.info("Loading config handler...")
  logging.basicConfig(level=logging.DEBUG)
  config = config_handler.Config()

  app.secret_key = config.get_string_value("site", "secret_key")
  app.config['SESSION_TYPE'] = config.get_string_value("site", "session_type")

  logging.info("Loading module handler...")
  module_handler = ModuleHandler()

  logging.info("Loading site modules...")
  module_handler.load_site_modules()

  logging.info("Warming up site modules...")
  module_handler.warmup_site_modules()

  logging.info("Starting site...")
  Flask.run(app, host=config.get_string_value("site", "bind_ip"), port=config.get_int_value("site", "bind_port"))

  logging.info("Shutting down site modules...")
  module_handler.shutdown_site_modules()

  logging.info("Done!")
