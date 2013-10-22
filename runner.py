import importlib # This should be installed for Python < 2.7
from amonagent.settings import settings
from amonagent.runner import runner
from amonagent.remote import remote



plugin_report = {}
for plugin in settings.PLUGINS:
	plugin_path = "amonagent.plugins.{0}".format(plugin)
	module = importlib.import_module(plugin_path)
	report = module.plugin.build_report()
	if len(report) > 0:
		plugin_report[plugin] = report
		
remote.save_plugin_stats(plugin_report)