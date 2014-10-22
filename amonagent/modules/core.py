import subprocess
import re
import requests

import logging
log = logging.getLogger(__name__)


from amonagent.utils import split_and_slugify, to_float

def get_cpu_info():
	processor_dict = {}

	with open('/proc/cpuinfo', 'r') as l:
		lines = l.readlines()

		for line in lines:
			parsed_line = split_and_slugify(line)
			if parsed_line and isinstance(parsed_line, dict):
				key = parsed_line.keys()[0]
				key = key.replace('-', '')
				value = parsed_line.values()[0]
				processor_dict[key] = value

	
	return processor_dict


def get_ip_address():	
	
	ip_address = ""
	try:
		response = requests.get('https://amon.cx/api/checkip?format=json', timeout=5)
	except:
		response = False

	if response:
		if response.status_code == 200:
			json = response.json()
			ip_address = json.get('ip')

	return ip_address


def get_uptime():
	uptime = ""
	
	with open('/proc/uptime', 'r') as line:
		contents = line.read().split()

	total_seconds = float(contents[0])

	MINUTE  = 60
	HOUR    = MINUTE * 60
	DAY     = HOUR * 24

	days    = int( total_seconds / DAY )
	hours   = int( ( total_seconds % DAY ) / HOUR )
	minutes = int( ( total_seconds % HOUR ) / MINUTE )
	seconds = int( total_seconds % MINUTE )

	uptime = "{0} days {1} hours {2} minutes {3} seconds".format(days, hours, minutes, seconds)

	return uptime



def get_memory_info():

	memory_dict = {}
	_save_to_dict = ['MemFree', 'MemTotal', 'SwapFree', 'SwapTotal', 'Buffers', 'Cached']

	regex = re.compile(r'([0-9]+)')

	with open('/proc/meminfo', 'r') as lines:

		for line in lines:
			values = line.split(':')
		
			match = re.search(regex, values[1])
			if values[0] in _save_to_dict:
				memory_dict[values[0].lower()] = int(match.group(0)) / 1024 # Convert to MB

		# Unix releases buffers and cached when needed
		buffers = memory_dict.get('buffers', 0)
		cached = memory_dict.get('cached', 0)

		memory_free = memory_dict['memfree']+buffers+cached
		memory_used = memory_dict['memtotal']-memory_free
		
		memory_percent_used = (float(memory_used)/float(memory_dict['memtotal'])*100)
		
		swap_total = memory_dict.get('swaptotal', 0)
		swap_free = memory_dict.get('swapfree', 0)
		swap_used = swap_total-swap_free
		swap_percent_used = 0
		
		if swap_total > 0:
			swap_percent_used = (float(swap_used)/float(swap_total) * 100)

		extracted_data = {
			"total_mb": memory_dict["memtotal"],
			"free_mb": memory_free,
			"used_mb": memory_used,
			"used_percent": memory_percent_used,
			"swap_total_mb":swap_total,
			"swap_free_mb": swap_free,
			"swap_used_mb": swap_used,
			"swap_used_percent": swap_percent_used
		}

		# Convert everything to int to avoid float localization problems
		for k,v in extracted_data.items():
			extracted_data[k] = int(v)
	   
		return extracted_data


class DiskCheck(object):


	def parse_output(self, df_output):

		all_devices = [l.strip().split() for l in df_output.split("\n")]

		# Skip the header row and empty lines.
		raw_devices = [l for l in all_devices[1:] if l]

		# Flatten the disks that appear in the mulitple lines.
		flattened_devices = self._flatten_devices(raw_devices)

		# Filter fake disks.
		def keep_device(device):
			if not self._is_real_device(device):
				return False
			return True
				   
		devices = filter(keep_device, flattened_devices)


		return devices


	def _is_number(a_string):
		try:
			float(a_string)
		except ValueError:
			return False
		
		return True


	def _check_blocks(self, blocks):
		try:
			number_of_block = float(blocks)
		except ValueError:
			return False

		if number_of_block == 0:
			return False

		return True

	def _is_real_device(self, device):
		"""
		Return true if we should track the given device name and false otherwise.
		"""
		# First, skip empty lines.
		if not device or len(device) <= 1:
			return False

		# Filter out fake devices.
		device_name = device[0]
		if device_name == 'none':
			return False

		# Now filter our fake hosts like 'map -hosts'. For example:
		#       Filesystem    1024-blocks     Used Available Capacity  Mounted on
		#       /dev/disk0s2    244277768 88767396 155254372    37%    /
		#       map -hosts              0        0         0   100%    /net
		blocks = device[1]

		try:
			number_of_block = float(blocks)
		except ValueError:
			return False

		if number_of_block == 0:
			return False

		return True


	def _flatten_devices(self, devices):
		# Some volumes are stored on their own line. Rejoin them here.
		previous = None
		for parts in devices:
			if len(parts) == 1:
				previous = parts[0]
			elif previous and self._is_number(parts[0]):
				# collate with previous line
				parts.insert(0, previous)
				previous = None
			else:
				previous = None
		return devices

	def check(self):
		data = {}


		try:
			df = subprocess.Popen(['df','-m'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]	
			dfi = subprocess.Popen(['df','-i'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]	
		except:
			log.exception('Unable to collect disk usage metrics.')
			return False


		inodes = self.parse_output(dfi)
		volumes = self.parse_output(df)

		_volume_columns = ('volume', 'total', 'used', 'free', 'percent', 'path')	
		_inode_columns = ('filesystem', 'inodes', 'iused', 'ifree', 'iuse%', 'mounted_on')	

		inode_dict =  map(lambda x: dict(zip(_inode_columns, x)), inodes)
		volumes_dict = map(lambda x: dict(zip(_volume_columns, x)), volumes)
		
		for v in volumes_dict:

			if v['volume'].startswith('/'):

				if any(i['filesystem'] == v['volume'] for i in inode_dict):

					# strip /dev/
					name = v['volume'].replace('/dev/', '')
					v['percent'] = to_float(v['percent'].replace("%",'')) # Delete the % sign for easier calculation later

					# Encrypted directories -> /home/something/.Private
					name = name.replace('.','') if '.' in name else name

					data[name] = v

		return data



def get_network_traffic():

	try:
		stats = subprocess.Popen(['sar','-n','DEV','1','1'], 
		stdout=subprocess.PIPE, close_fds=True)\
			.communicate()[0]
	except:
		log.exception('Unable to collect network metrics.')
		return False

	network_data = stats.splitlines()
	data = {}
	for line in network_data:
		if line.startswith('Average'):
			elements = line.split()
			interface = elements[1]
			
			# interface name with . 
			if '.' in interface:
				interface = interface.replace('.','-')

			if interface not in ['IFACE', 'lo']:
				# rxkB/s - Total number of kilobytes received per second  
				# txkB/s - Total number of kilobytes transmitted per second
				
				inbound = to_float(elements[4])
				inbound = "{0:.2f}".format(inbound)

				outbound = to_float(elements[5])
				outbound = "{0:.2f}".format(outbound)

				data[interface] = {"inbound": inbound , "outbound": outbound}


	return data

 
def get_load_average():
	_loadavg_columns = ['minute','five_minutes','fifteen_minutes']
	load_dict = {}


	with open('/proc/loadavg', 'r') as l:
		lines = l.readlines()
		load_data = lines[0].split()

		_loadavg_values = load_data[:4]

		load_dict = dict(zip(_loadavg_columns, _loadavg_values))	


	# Get cpu cores 
	with open('/proc/cpuinfo', 'r') as l:
		lines = l.readlines()

		for line in lines:
			if 'cores' in line:
				cores = re.findall(r'\d+', line)

	try:
		load_dict['cores'] = int(cores[0])
	except:
		load_dict['cores'] = 1 # Don't break if can't detect the cores 

	return load_dict 


def get_cpu_utilization():

	# Get the cpu stats
	try:
		mpstat = subprocess.Popen(['sar', '1','1'], 
		stdout=subprocess.PIPE, close_fds=True).communicate()[0]
	except:
		log.exception('Unable to collect CPU metrics.')
		return False

	cpu_columns = []
	cpu_values = []
	header_regex = re.compile(r'.*?([%][a-zA-Z0-9]+)[\s+]?') # the header values are %idle, %wait
	
	# International float numbers - could be 0.00 or 0,00
	value_regex = re.compile(r'\d+[\.,]\d+') 
	stats = mpstat.split('\n')

	for value in stats:
		values = re.findall(value_regex, value)
		if len(values) > 4:
			values = map(lambda x: to_float(x), values) # Replace , with . if necessary
			cpu_values = map(lambda x: format(float(x), ".2f"), values) # Convert the values to float with 2 points precision

		header = re.findall(header_regex, value)
		if len(header) > 4:
			cpu_columns = map(lambda x: x.replace('%', ''), header) 

	cpu_dict = dict(zip(cpu_columns, cpu_values))
	
	return cpu_dict


disk_check = DiskCheck()