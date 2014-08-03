try:
	import json
except ImportError:
	import simplejson as json

import os

try:
	config_file = file('/etc/amon-agent.conf').read()
	config = json.loads(config_file)
except Exception, e:
	print "There was an error in your configuration file (/etc/amon-agent.conf)"
	raise e


# 1 minute default
SYSTEM_CHECK_PERIOD = config.get('system_check_period', 60)


HOST = config.get('host', 'https://amon.cx')


SERVER_KEY = config.get('server_key', None)

if os.path.exists('/var/run/amonagent/'):
	PIDFILE = '/var/run/amonagent/amonagent.pid'
else:
	PIDFILE = config.get('pidfile', '/var/run/amonagent.pid')

# LOGGING DEFAULTS 
LOGFILE = config.get("logfile", '/var/log/amonagent/amonagent.log')
LOGGING_MAX_BYTES = 5 * 1024 * 1024