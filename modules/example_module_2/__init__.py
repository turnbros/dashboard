from modules import Module
import http.client
import json

class Main(Module):

  def __init__(self):
    super().__init__(
      index=2,
      name="example_module_2",
      title="Example Module 2",
      icon="fa fa-connectdevelop",
      path=f"{str(__name__).replace('.', '/')}"
    )

  def handle_request(self, **kwargs):
    print("Handle Request")
    api_url = self._config.get_string_value("api", "api_base_url")
    tenant = "test-tenant-1"
    url = f"/tenant/{tenant}/resource"

    print(f"API URL: {api_url}")
    print(f"Tenant: {tenant}")
    print(f"URL: {url}")

    conn = http.client.HTTPConnection(api_url)
    conn.request("GET", url)

    r2 = conn.getresponse()
    print(f"R2:{r2}")

    r2_json = json.loads(r2.read())
    print(f"R2 JSON: {r2_json}")
    tenant_resources = r2_json["resources"]

    data_rows = []
    for resource in tenant_resources:
      data_rows.append({
        "name" : resource["name"],
        "module" : resource["module"],
        "status" : resource["status"]
      })
    print(f"Data Rows: {data_rows}")


    conn = http.client.HTTPConnection(api_url)
    conn.request("GET", "/workspace/manifest")
    module_manifest = json.loads(conn.getresponse().read())
    return {
      "module_name": self.name,
      "module_manifest": json.dumps(module_manifest),
      "data_rows": data_rows
    }
