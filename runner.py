import sys
sys.path.insert(0, '/home/martin/amonagent')

from amonagent.plugin import discover_plugins


plugins = discover_plugins(plugin_paths=['/home/martin/temp/checks'])

for plugin in plugins:
	plugin.run()