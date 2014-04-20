from amonagent import defaults


try:
	import json
except ImportError:
	import simplejson as json

try:
	config_file = file('/etc/amon-agent.conf').read()
	config = json.loads(config_file)
except Exception, e:
	print "There was an error in your configuration file (/etc/amon-agent.conf)"
	raise e




class Settings(object):

	def __init__(self):
		# update this dict from the defaults dictionary (but only for ALL_CAPS settings)
		for setting in dir(defaults):
			if setting == setting.upper():
				setattr(self, setting, getattr(defaults, setting))

settings = Settings()

