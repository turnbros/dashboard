import json
from util import request

def get_resources(tenant_name):
  response = request.send_api_request(f"/tenant/{tenant_name}/resource")
  print(f"response:{response}")
  response_json = json.loads(response.read())
  print(f"Response JSON: {response_json}")
  return response_json["resources"]

def get_module_resources(tenant_name, module_name):
  response = request.send_api_request(f"/tenant/{tenant_name}/resource?module={module_name}")
  print(f"response:{response}")
  response_json = json.loads(response.read())
  print(f"Response JSON: {response_json}")
  return response_json["resources"]
