import subprocess
import os

def install(plugin_name):

	BASE_PLUGIN_PATH = "/etc/amonagent/plugins"

	PLUGIN_PATH = os.path.join(BASE_PLUGIN_PATH, plugin_name) 

	if os.path.exists(PLUGIN_PATH):

		plugin_name_with_ext = "{0}.yml".format(plugin_name)
		PLAYBOOK = os.path.join(PLUGIN_PATH, plugin_name_with_ext) 

	
		install_command = [
			'ansible-playbook',
			PLAYBOOK, 
			'-i',
			'/etc/amonagent/plugins/hosts'

		]

		result = subprocess.Popen(install_command, 
				stdout=subprocess.PIPE, 
				close_fds=True, 
		).communicate()[0]

		print result
	
	else:
		IGNORED_DIRS = ['.git']
		print "Invalid Plugin name. You can install the following plugins: "
		for name in os.listdir(BASE_PLUGIN_PATH):
			if os.path.isdir(os.path.join(BASE_PLUGIN_PATH, name)) and name not in IGNORED_DIRS:
				print name