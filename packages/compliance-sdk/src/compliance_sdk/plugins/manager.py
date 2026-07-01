import importlib
import os
from typing import List
from . import BasePlugin

class PluginManager:
    def __init__(self, plugin_paths: List[str] = None):
        self.plugins: List[BasePlugin] = []
        if plugin_paths:
            for path in plugin_paths:
                self.load_plugin(path)

    def load_plugin(self, path: str):
        module_name = os.path.basename(path).replace(".py", "")
        spec = importlib.util.spec_from_file_location(module_name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for attr in dir(module):
            obj = getattr(module, attr)
            if isinstance(obj, type) and issubclass(obj, BasePlugin) and obj is not BasePlugin:
                self.plugins.append(obj())

    async def execute(self, document: dict) -> dict:
        for plugin in self.plugins:
            document = await plugin.process(document)
        return document
