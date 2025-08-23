from typing import List
import pkg_resources

from graph_explorer_api.plugins.visualizer_plugin import VisualizerPlugin 

class PluginService(object):

    def __init__(self):
        self.plugins: dict[str,List[VisualizerPlugin]] = {}

    def load_plugins(self, group: str):
        """
        Dynamically loads plugins based on entrypoint group.
        """
        print("Group name: " + group)
        self.plugins[group] = []
        for entry in pkg_resources.iter_entry_points(group=group):
            print(f"Found {entry.name} plugin")
            p = entry.load()
            plugin = p()
            self.plugins[group].append(plugin)