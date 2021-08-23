import http.client
import config_handler

def send_api_request(request_url):
  config = config_handler.Config()
  api_url = config.get_string_value("api", "api_base_url")
  conn = http.client.HTTPConnection(api_url)
  conn.request("GET", request_url)
  print(f"URL: {api_url}/{request_url}")
  response = conn.getresponse()
  print(f"response:{response}")
  return response
