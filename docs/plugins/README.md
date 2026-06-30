# Plugin Architecture

## Overview
Lexicon supports custom processing steps via plugins.

## Creating a Plugin
1. Create a Python file with a class that inherits from `compliance_sdk.plugins.BasePlugin`.
2. Implement the `process` method.
3. Place the file in `services/<service>/plugins/`.
4. The service will automatically load all plugins from its `plugins` directory.

## Example
See `services/compliance-engine/plugins/example_plugin.py`.
