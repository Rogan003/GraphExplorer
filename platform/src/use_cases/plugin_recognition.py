from typing import List
import pkg_resources

from graph_explorer_api.plugins.base import Plugin

class PluginService(object):

    def __init__(self):
        self.plugins: dict[str,List[Plugin]] = {}

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

    def get_selected_plugin(self, group: str, identifier: str) -> Plugin:
        if identifier:
            for plugin in self.plugins[group]:
                if plugin.identifier() == identifier:
                    return plugin

        return self.plugins[group][0] if self.plugins[group] else None