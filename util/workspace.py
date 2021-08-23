import http.client
import json
import config_handler

def get_manifest():
  config = config_handler.Config()
  api_url = config.get_string_value("api", "api_base_url")
  conn = http.client.HTTPConnection(api_url)
  conn.request("GET", "/workspace/manifest")
  return json.loads(conn.getresponse().read())
