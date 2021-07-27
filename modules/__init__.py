import os
import logging
import config_handler
from jinja2 import Template


class Module(object):

  def __init__(self, index, name, title, icon, path):

    self._config = config_handler.Config()
    self._module_styles_dir = f"{path}/styles"
    self._module_scripts_dir = f"{path}/scripts"

    self._index = index
    self._name = name
    self._title = title
    self._icon = icon
    self._path = path
    self._module_styles = {}
    self._module_scripts = {}
    self._module_styles_list = []
    self._module_scripts_list = []

    with open(f"{path}/index.html") as module_template:
      self._template = module_template.read()

    if os.path.isdir(self._module_styles_dir):
      for module_style in next(os.walk(self._module_styles_dir))[2]:
        with open(f"{self._module_styles_dir}/{module_style}") as module_style_file:
          self._module_styles[module_style] = module_style_file.read()
          self._module_styles_list.append(f"{self._module_styles_dir}/{module_style}")

    if os.path.isdir(self._module_scripts_dir):
      for module_script in next(os.walk(self._module_scripts_dir))[2]:
        with open(f"{self._module_scripts_dir}/{module_script}") as module_script_file:
          self._module_scripts[module_script] = module_script_file.read()
          self._module_scripts_list.append(f"{self._module_scripts_dir}/{module_script}")

  @property
  def index(self):
    return self._index

  @property
  def name(self):
    return self._name

  @property
  def title(self):
    return self._title

  @property
  def icon(self):
    return self._icon

  @property
  def template(self):
    return self._template

  @property
  def module_styles(self):
    return self._module_styles_list

  @property
  def module_scripts(self):
    return self._module_scripts_list

  def get_module_style(self, style_name):
    return self._module_styles[style_name]

  def get_module_script(self, script_name):
    return self._module_scripts[script_name]

  def render(self, **kwargs):
    template_data = {}
    try:
      template_data = self.handle_request(**kwargs)
    except Exception as e:
      logging.error(f"Failure while rendering module {self.name}: {e.message}")
    finally:
      return Template(self.template).render(module_content=template_data)

  def handle_request(self, **kwargs):
    pass

  def warmup(self):
    pass

  def shutdown(self):
    pass


class ModuleHandler(object):
  def __init__(self):
    self._site_modules = dict()
    self._sorted_site_module_list = []
    self._config = config_handler.Config()

  @property
  def site_modules(self):
    return self._site_modules

  @property
  def sorted_site_module_list(self):
    return self._sorted_site_module_list

  def load_site_modules(self, module_directory="modules"):
    temp_site_module_list = []
    module_list = next(os.walk(module_directory))
    for site_module_string in module_list[1]:
      if site_module_string[:2] != "__":
        try:
          site_module_import = __import__("modules.{}".format(site_module_string), fromlist=["modules"])
          site_module_instance = site_module_import.Main()

          temp_site_module_list.append({
            "index": site_module_instance.index,
            "name": site_module_instance.name,
            "title": site_module_instance.title,
            "icon": site_module_instance.icon
          })

          self.site_modules[site_module_string] = site_module_instance

        except Exception as error:
          logging.error(f"Failed to import site module: {site_module_string}: {error.with_traceback()}")

    self._sorted_site_module_list = sorted(temp_site_module_list, key=lambda k: k['index'])

  def warmup_site_modules(self):
    for site_module in self.site_modules.keys():
      logging.info(f"Warming up site module: {site_module}")
      logging.debug(self.site_modules.get(site_module).warmup())

  def shutdown_site_modules(self):
    for site_module in self.site_modules.keys():
      logging.info(f"Shutting down site module: {site_module}")
      logging.debug(self.site_modules.get(site_module).shutdown())

  def render_module(self, module_name, user_session, **kwargs):

    if module_name is None:
      module_name = self.sorted_site_module_list[0]["name"]

    with open("static/html/site_template.html") as site_template:
      try:
        called_module = self.site_modules.get(module_name)

        if called_module is None:
          return None

        try:
          return Template(site_template.read()).render(site_title=self._config.get_string_value("site", "title"),
                                                       site_name_1=self._config.get_string_value("site", "name_1"),
                                                       site_name_2=self._config.get_string_value("site", "name_2"),
                                                       session_profile=user_session,
                                                       active_module=module_name,
                                                       module_list=self.sorted_site_module_list,
                                                       module_title=called_module.title,
                                                       module_content=called_module.render(**kwargs),
                                                       module_styles=called_module.module_styles,
                                                       module_scripts=called_module.module_scripts)

        except Exception as no_session:
          logging.error(no_session)

      except ImportError as error:
        logging.error("Failed to import: ", module_name)
        logging.error(error)

      return None
