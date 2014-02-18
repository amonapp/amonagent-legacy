import imp
import os

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
			cls.register_plugin(cls)
 
	def register_plugin(cls, plugin):
		"""Add the plugin to the plugin list and perform any registration logic"""
 
		# create a plugin instance and store it
		# optionally you could just store the plugin class and lazily instantiate
		instance = plugin()
 
		# save the plugin reference
		cls.plugins.append(instance)
 

class AmonPlugin(object):
	__metaclass__ = PluginMount



def discover_plugins(plugin_paths=[]):
	""" Discover the plugin classes contained in Python files, given a
		list of directory names to scan. Return a list of plugin classes.
	"""
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