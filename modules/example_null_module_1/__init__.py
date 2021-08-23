from modules import Module
import json
from util import tenant
from util import workspace
from util.config import config

class Main(Module):

  def __init__(self):
    super().__init__(
      path=f"{str(__name__).replace('.', '/')}"
    )

    self.tenant_name = "test-tenant-1"
    self.module_name = "example_null_module_1"

    self.workspace_manifest = workspace.get_manifest()
    self.index = self.workspace_manifest[self.module_name]['index']
    self.name = self.workspace_manifest[self.module_name]['name']
    self.title = self.workspace_manifest[self.module_name]['title']
    self.icon = self.workspace_manifest[self.module_name]['icon']

  def handle_request(self, **kwargs):
    print("Handle Request")
    data_rows = []
    for resource in tenant.get_module_resources(self.tenant_name, self.module_name):
      if resource["status"] not in ["Purge Error", "Purged"]:
        data_rows.append({
          "name" : resource["name"],
          "module" : resource["module"],
          "status" : resource["status"]
        })

    return {
      "tenant_name": self.tenant_name,
      "module_name": self.name,
      "module_manifest": json.dumps(workspace.get_manifest()),
      "data_rows": data_rows,
      "api_endpoint": config.get_string_value("api", "api_base_url")
    }
