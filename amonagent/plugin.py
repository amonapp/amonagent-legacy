import imp
import os
import re

from amonagent.log import logging
try:
	import json
except ImportError:
	import simplejson as json

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
		default_path = '/etc/amonagent/config/'
		filename = "{0}{1}.conf".format(default_path, self.name)
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

	def __init__(self, name):
		self.name = name
		self.log = logging.getLogger('%s.%s' % (__name__, name))
		self.config = self._get_configuration_file()
		self.result = {'gauges': {}, 'counters': {}}

	def collect(self):
		raise NotImplementedError


def discover_plugins(plugin_paths=[]):
	""" Discover the plugin classes contained in Python files, given a
		list of directory names to scan. Return a list of plugin classes.
	"""
	if len(plugin_paths) == 0:
		plugin_paths = ['/etc/amonagent/plugins']

	for directory in plugin_paths:
		for filename in os.listdir(directory):
			modname, ext = os.path.splitext(filename)
			if ext == '.py':
				_file, path, descr = imp.find_module(modname, [directory])
				if _file:
					# Loading the module registers the plugin in
					if modname not in ['base', '__init__']:
						mod = imp.load_module(modname, _file, path, descr)

	return AmonPlugin.plugins