from compliance_sdk.plugins import BasePlugin

class ExamplePlugin(BasePlugin):
    async def process(self, document):
        document["plugin_processed"] = True
        return document
