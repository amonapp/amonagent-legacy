import sys
sys.path.insert(0, '/home/martin/amonagent')

from amonagent.plugin import discover_plugins


plugins = discover_plugins()

for plugin in plugins:
	plugin.collect()
	print plugin.name
	print plugin.result
	