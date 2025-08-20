from django.apps import AppConfig
from use_cases.plugin_recognition import PluginService
from use_cases.const import VISUALIZER_GROUP

visualizer_group = VISUALIZER_GROUP

class GraphExplorerConfig(AppConfig):
  default_auto_field = 'django.db.models.BigAutoField'
  name = 'graph_explorer'
  plugin_service = PluginService()

  def ready(self):
    # On aplication start load all plugins
    self.plugin_service.load_visualizer_plugins(VISUALIZER_GROUP)
    