import re
import subprocess

from amonagent.modules.distro import get_distro
from amonagent.utils import unix_utc_now


class SystemPackages(object):

	def __init__(self):
		distro = get_distro()

		# apt or yum
		self.distro_type = distro.get('type')
		self.next_run = unix_utc_now()



	def apt_updates(self):
		# Update repository info only once per 24 hours
		now  = unix_utc_now()
		if now > self.next_run:
			self.next_run = now+86400
			subprocess.Popen(["apt-get",'update'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]



		packages_for_upgrade = subprocess.Popen(["apt-get",'-q','-V', '-s', 'upgrade', '2>&1 /dev/null'], stdout=subprocess.PIPE, close_fds=True,
						).communicate()[0]


		packages_for_upgrade_list = []
		upgrades_index = False
		for index, line in enumerate(packages_for_upgrade.splitlines()):
			if line.startswith('The following packages will be upgraded'):
				upgrades_index = True

			if upgrades_index is True:
				
				regex = re.compile(r'^\s+(\S+)\s+\((\S+)\s+=>\s+(\S+)\)')
				match = regex.match(line)

				if match:
					name, current_version, new_version = match.groups()

					package_dict = {'name': name, 
							'current_version': current_version,
							'new_version': new_version
						}
						
					packages_for_upgrade_list.append(package_dict)


		return packages_for_upgrade_list


	def yum_updates(self):

		installed_packages_dict = {}
		installed_packages = subprocess.Popen(["yum",'--color=never','list', 'installed'], stdout=subprocess.PIPE, 
			close_fds=True).communicate()[0]


		for line in installed_packages.splitlines():
			regex = re.compile(r'^(.*?)\s+(.*?)\s+@(.*)$')
			match = regex.match(line)
			if match:
				name, version, repo = match.groups()
				installed_packages_dict[name] = version



		packages_for_upgrade_list = []
		packages_for_upgrade = subprocess.Popen(["yum",'check-update'], stdout=subprocess.PIPE, close_fds=True,
								).communicate()[0]


		for line in packages_for_upgrade.splitlines():
			regex = re.compile(r'^(\S+\.\S+)\s+(\S+)\s+\S+$')
			match = regex.match(line)
			if match:
				name, new_version = match.groups()

				# Check if this version is new 
				currently_installed_version = installed_packages_dict.get(name)
				if currently_installed_version != None:

					if currently_installed_version != new_version:
						
						package_dict = {'name': name, 
							'current_version': currently_installed_version,
							'new_version': new_version
						}
						
						packages_for_upgrade_list.append(package_dict)


		return packages_for_upgrade_list



	def result(self):
		
		result = None

		if self.distro_type == 'apt':
			result = self.apt_updates()
		elif self.distro_type == 'yum':
			result = self.yum_updates()

		return result



system_packages = SystemPackages()