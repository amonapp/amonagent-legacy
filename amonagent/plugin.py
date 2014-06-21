import imp
import os
import re
import logging

try:
	import json
except ImportError:
	import simplejson as json

# CONSTANTS
AMONAGENT_PATH = "/etc/amonagent"
ENABLED_PLUGINS_PATH = "{0}/plugins-enabled".format(AMONAGENT_PATH)
AVAILABLE_PLUGINS_PATH	= "{0}/plugins".format(AMONAGENT_PATH)

class PluginMount(type):
	"""
	A plugin mount point derived from:
		http://martyalchin.com/2008/jan/10/simple-plugin-framework/
	Acts as a metaclass which creates anything inheriting from Plugin
	"""
 
	def __init__(cls, name, bases, attrs):
		"""Called when a Plugin derived class is imported"""
 
		if not hasattr(cls, 'plugins'):
			# Called when the metaclass is first instantiated
			cls.plugins = []
		else:
			# Called when a plugin class is imported
			name  = attrs["__module__"]

			cls.register_plugin(cls, name)
 
	def register_plugin(cls, plugin, name):
		"""Add the plugin to the plugin list and perform any registration logic"""
 
		# create a plugin instance and store it
		# optionally you could just store the plugin class and lazily instantiate
		instance = plugin(name)
 
		# save the plugin reference
		cls.plugins.append(instance)
 

class AmonPlugin(object):

	__metaclass__ = PluginMount


	def _get_configuration_file(self):
		
		filename = "{0}/{1}.conf".format(ENABLED_PLUGINS_PATH, self.name)
		config = {}
		
		try:
			config_file = file(filename).read()
			config = json.loads(config_file)
		except Exception, e:
			print "There was an error in your configuration file ({0})".format(filename)
			raise e
		
		return config


	def normalize(self, metric, prefix=None):
		"""Turn a metric into a well-formed metric name
		prefix.b.c
		"""
		name = re.sub(r"[,\+\*\-/()\[\]{}]", "_", metric)
		# Eliminate multiple _
		name = re.sub(r"__+", "_", name)
		# Don't start/end with _
		name = re.sub(r"^_", "", name)
		name = re.sub(r"_$", "", name)
		# Drop ._ and _.
		name = re.sub(r"\._", ".", name)
		name = re.sub(r"_\.", ".", name)

		if prefix is not None:
			return prefix + "." + name
		else:
			return name

	def counter(self, name, value):
		name = self.normalize(name)
		
		self.result['counters'][name] = value

	def gauge(self, name, value):
		name = self.normalize(name)

		self.result['gauges'][name] = value


	def version(self, library=None, plugin=None, **kwargs):

		if library:
			self.result['versions']['library'] = library
		if plugin:
			self.result['versions']['plugin'] = plugin

		if kwargs:
			for k,v in kwargs.items():
				self.result['versions'][k] = v

	def __init__(self, name):
		self.name = name

		self.config = self._get_configuration_file()
		self.log = logging.getLogger('%s.%s' % (__name__, name))
		self.result = {'gauges': {}, 'counters': {}, 'versions': {}}

	def collect(self):
		raise NotImplementedError


def discover_plugins(plugin_paths=[]):
	""" Discover the plugin classes contained in Python files, given a
		list of directory names to scan. Return a list of plugin classes.
		
		For now this method will look only in /etc/amonagent/plugins with possible 
		future extension which will permit searching for plugins in 
		user defined directories
	"""
	if os.path.exists(ENABLED_PLUGINS_PATH):
		# Find all enabled plugins
		for filename in os.listdir(ENABLED_PLUGINS_PATH):
			plugin_name, ext = os.path.splitext(filename)
			if ext == ".conf":
				# Configuration file OK, load the plugin
				full_plugin_path = "{0}/{1}".format(AVAILABLE_PLUGINS_PATH, plugin_name)

				for filename in os.listdir(full_plugin_path):
					modname, extension = os.path.splitext(filename)
					if extension == '.py':
						_file, path, descr = imp.find_module(modname, [full_plugin_path])
						if _file:
							# Loading the module registers the plugin in
							if modname not in ['base', '__init__']:
								mod = imp.load_module(modname, _file, path, descr)
			
	return AmonPlugin.plugins