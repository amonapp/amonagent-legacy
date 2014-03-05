import sys
sys.path.insert(0, '/home/martin/amonagent')

from amonagent.plugin import discover_plugins


plugins = discover_plugins()

# for plugin in plugins:
# 	plugin.collect()
# 	print plugin.name
# 	print plugin.result


plugin_result_dict = {}
for plugin in plugins:
	plugin.collect()
	plugin_result_dict[plugin.name] = plugin.result

print plugin_result_dict