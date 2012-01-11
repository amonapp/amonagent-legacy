import sys
try:
    import json
except ImportError:
    import simplejson as json

try:
	config_file = file('/etc/amon-agent.conf').read()
	config = json.loads(config_file)
except:
	config = {}

#  Amon agent Defaults
_remote = config.get('remote', {})

# 1 minute default
SYSTEM_CHECK_PERIOD = config.get('system_check_period', 60)

SYSTEM_CHECKS = ['cpu', 'memory', 'disk', 'network', 'loadavg']

if sys.platform == 'darwin':
	del SYSTEM_CHECKS[3] # Don't check the network on MacOS

PROCESS_CHECKS = config.get('process_checks', [])


host = _remote.get('host', 'http://127.0.0.1')

if not host.startswith('http'):
	host = "http://{0}".format(host)

REMOTE = {
	'host': host,
	'port': _remote.get('port', 2464)
}

SERVER_KEY = config.get('server_key', None)

CACHE_DIR = config.get('cache_dir', '/usr/local/amon/')
