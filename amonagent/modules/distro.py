import os 
import re 
import platform


REPORTED_FIELDS = [
	'description', 
	'release',
	'codename',
	'id',
	'name'
]


OSDIST_LIST = ( 
	('/etc/redhat-release', 'RedHat'),
	('/etc/system-release', 'OtherLinux'),
	('/etc/os-release', 'Debian'),
	('/etc/lsb-release', 'Mandriva'),
	('/etc/debian_version', 'Ubuntu'),
	('/etc/centos-release','CentOS') 
)


PKG_MGRS = [ 
	{'path' : '/usr/bin/yum', 'name' : 'yum'},
	{'path' : '/usr/bin/apt-get', 'name' : 'apt'},
]


# Make it testable 
def parse_distro_file(lines=None):
	distro = {}
	
	for line in lines:
		
		# Barebones match: 
		# CentOS release 6.5 (Final)
		find_release = re.compile(r'\d+\.\d+')
		release = find_release.search(line)

		if release is not None:
			distro['release'] = release.group()


		# Matches any possible format:
		#     DISTRIB_ID="Ubuntu"
		#     DISTRIB_ID='Mageia'
		#     DISTRIB_ID=Fedora
		#     DISTRIB_RELEASE='10.10'
		#     DISTRIB_CODENAME='squeeze'
		#     DISTRIB_DESCRIPTION='Ubuntu 10.10'
		regex = re.compile('^(DISTRIB_(?:ID|RELEASE|CODENAME|DESCRIPTION))=(?:\'|")?([\\w\\s\\.-_]+)(?:\'|")?')
		match = regex.match(line.rstrip('\n'))
		if match:

			distro_key = '{0}'.format(match.groups()[0].lower())
			distro_key = distro_key.replace('distrib_', "")

			if distro_key in REPORTED_FIELDS:
				distro[distro_key] = match.groups()[1].rstrip()

		# Matches any possible format:
		# PRETTY_NAME="Debian GNU/Linux 7 (wheezy)"
		# NAME="Debian GNU/Linux"
		# VERSION_ID="7"
		# VERSION="7 (wheezy)"
		# ID=debian
		# ANSI_COLOR="1;31"
		# HOME_URL="http://www.debian.org/"
		# SUPPORT_URL="http://www.debian.org/support/"
		# BUG_REPORT_URL="http://bugs.debian.org/"
		regex = re.compile('^([\\w]+)=(?:\'|")?([\\w\\s\\.-_]+)(?:\'|")?')
		match = regex.match(line.rstrip('\n'))
		if match:
			name, value = match.groups()
			formated_name = name.lower()

			if formated_name in REPORTED_FIELDS:
				distro[formated_name] = value


	# Check for data in the distro dict and if empty - try collecting data with Python
	release = distro.get('release')

	distro_info = []
	if release == None:
		
		try: 
			distro_info = platform.dist() # Deprecated in Python 2.6
		except:
			distro_info = platform.linux_distribution()

	# (distname,version,id)
	if len(distro_info) == 3:
		distro['name'], distro['release'], distro['id'] = distro_info

	return distro


def get_distro():

	distro = {}

	for pm in PKG_MGRS:
		if os.path.isfile(pm['path']):
			distro['type'] =  pm['name']

	
	for (path, name) in OSDIST_LIST:
		if os.path.isfile(path) and os.path.getsize(path) > 0:

			# Set it once, just in case, overwrite later 
			distro['name'], distro['id'] = name, name.lower()

			lines = []
			with open(path) as f:
				for line in f:
					lines.append(line)

			result = parse_distro_file(lines=lines)	

			distro.update(result)

	

	return distro