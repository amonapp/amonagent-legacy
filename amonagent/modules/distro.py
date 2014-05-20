import os 
import re 

def get_distro():
	distro = {}
	try:
		import lsb_release
		release = lsb_release.get_distro_information()
		for key, value in release.iteritems():
			key = key.lower()
			if key == 'id':
				distro['id'] = value.lower()
			if key == 'release':
				distro['release'] = value
		
		distro['type'] = 'apt'

	except ImportError:
		# if the python library isn't available, default to regex
		if os.path.isfile('/etc/lsb-release'):
			with open('/etc/lsb-release') as ifile:
				for line in ifile:
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
						
						# Adds: lsb_distrib_{id,release,codename,description}
						distro_key = '{0}'.format(match.groups()[0].lower())
						distro_key = distro_key.replace('distrib_', "")
						distro[distro_key] = match.groups()[1].rstrip()
			
			distro['type'] = 'apt'
		
		# Debian 
		elif os.path.isfile('/etc/debian_version'):
			with open('/etc/debian_version') as ifile:
					for line in ifile:
						find_release = re.compile(r'\d+\.\d+')
						release = find_release.search(line)
						if release is not None:
							distro['release'] = release.group()
							distro['type'] = 'apt'
							distro['id'] = 'debian'
		elif os.path.isfile('/etc/centos-release'):
			# CentOS Linux
			distro['id'] = 'centos'
			with open('/etc/centos-release') as ifile:
				for line in ifile:
					find_release = re.compile(r'\d+\.\d+')
					release = find_release.search(line)
					if release is not None:
						distro['release'] = release.group()
						distro['type'] = 'yum'

		elif os.path.isfile('/etc/os-release'):
			# Arch Linux and Fedora
			with open('/etc/os-release') as ifile:
				for line in ifile:
					# NAME="Arch Linux ARM"
					# VERSION_ID="7"
					# VERSION="7 (wheezy)"
					# ID=archarm
					# ID_LIKE=arch
					# PRETTY_NAME="Arch Linux ARM"
					# ANSI_COLOR="0;36"
					# HOME_URL="http://archlinuxarm.org/"
					# SUPPORT_URL="https://archlinuxarm.org/forum"
					# BUG_REPORT_URL="https://github.com/archlinuxarm/PKGBUILDs/issues"
					regex = re.compile('^([\\w]+)=(?:\'|")?([\\w\\s\\.-_]+)(?:\'|")?')
					match = regex.match(line.rstrip('\n'))
					if match:
						name, value = match.groups()
						if name.lower() == 'version':
							distro['release'] = value.strip()
						if name.lower() == 'name':
							distro['id'] = value.strip().lower()
		elif os.path.isfile('/etc/system-release'):
			# Amazon Linux AMI
			distro['id'] = 'amazon'
			distro['type'] = 'yum'
			with open('/etc/system-release') as ifile: 
				for line in ifile:
					find_release = re.compile(r'\d+\.\d+')
					release = find_release.search(line)
					if release is not None:
						distro['release'] = release.group()

	return distro