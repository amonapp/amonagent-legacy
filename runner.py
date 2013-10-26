import importlib # This should be installed for Python < 2.7
from amonagent.settings import settings
from amonagent.remote import remote
import time


def main():
	while  True:
		plugin_report = {}
		for plugin in settings.PLUGINS:
			plugin_path = "amonagent.plugins.{0}".format(plugin)
			module = importlib.import_module(plugin_path)
			report = module.plugin.build_report()
			if len(report) > 0:
				plugin_report[plugin] = report
		
			remote.save_plugin_stats(plugin_report)
			
			# Clear the dictionary
			try:
				del plugin_report[plugin]
			except: 
				pass
		print "report sent for {0}".format(plugin)
		time.sleep(10)

if __name__ == "__main__":
	main()