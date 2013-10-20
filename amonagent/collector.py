import subprocess
import re

class LinuxSystemCollector(object):


	def get_uptime(self):

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



	def get_memory_info(self):

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


	def get_disk_usage(self):
		df = subprocess.Popen(['df','-h'], stdout=subprocess.PIPE, close_fds=True).communicate()[0]	

		volumes = df.split('\n')	
		volumes.pop(0)	# remove the header
		volumes.pop()

		data = {}

		_columns = ('volume', 'total', 'used', 'free', 'percent', 'path')	

		previous_line = None

		for volume in volumes:
			line = volume.split(None, 6)

			if len(line) == 1: # If the length is 1 then this just has the mount name
				previous_line = line[0] # We store it, then continue the for
				continue

			if previous_line != None: 
				line.insert(0, previous_line) # then we need to insert it into the volume
				previous_line = None # reset the line

			if line[0].startswith('/'):
				_volume = dict(zip(_columns, line))

				_volume['percent'] = _volume['percent'].replace("%",'') # Delete the % sign for easier calculation later

				# strip /dev/
				_name = _volume['volume'].replace('/dev/', '')

				# Encrypted directories -> /home/something/.Private
				if '.' in _name:
					_name = _name.replace('.','')

				data[_name] = _volume

		return data



	def get_network_traffic(self):

		stats = subprocess.Popen(['sar','-n','DEV','1','1'], 
			stdout=subprocess.PIPE, close_fds=True)\
				.communicate()[0]
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
					
					inbound = elements[4].replace(',', '.')
					inbound = "{0:.2f}".format(float(inbound))

					outbound = elements[5].replace(',', '.')
					outbound = "{0:.2f}".format(float(outbound))

					data[interface] = {"inbound": inbound , "outbound": outbound}


		return data

	 
	def get_load_average(self):
		_loadavg_columns = ['minute','five_minutes','fifteen_minutes']


		lines = open('/proc/loadavg','r').readlines()

		load_data = lines[0].split()

		_loadavg_values = load_data[:4]

		load_dict = dict(zip(_loadavg_columns, _loadavg_values))	


		# Get cpu cores 
		cpuinfo = subprocess.Popen(['cat', '/proc/cpuinfo'], stdout=subprocess.PIPE, close_fds=True)
		grep = subprocess.Popen(['grep', 'cores'], stdin=cpuinfo.stdout, stdout=subprocess.PIPE, close_fds=True)
		sort = subprocess.Popen(['sort', '-u'], stdin=grep.stdout, stdout=subprocess.PIPE, close_fds=True)\
				.communicate()[0]

		cores = re.findall(r'\d+', sort) 

		try:
			load_dict['cores'] = int(cores[0])
		except:
			load_dict['cores'] = 1 # Don't break if can't detect the cores 

		return load_dict 


	def get_cpu_utilization(self):

		# Get the cpu stats
		mpstat = subprocess.Popen(['sar', '1','1'], 
			stdout=subprocess.PIPE, close_fds=True).communicate()[0]

		cpu_columns = []
		cpu_values = []
		header_regex = re.compile(r'.*?([%][a-zA-Z0-9]+)[\s+]?') # the header values are %idle, %wait
		# International float numbers - could be 0.00 or 0,00
		value_regex = re.compile(r'\d+[\.,]\d+') 
		stats = mpstat.split('\n')

		for value in stats:
			values = re.findall(value_regex, value)
			if len(values) > 4:
				values = map(lambda x: x.replace(',','.'), values) # Replace , with . if necessary
				cpu_values = map(lambda x: format(float(x), ".2f"), values) # Convert the values to float with 2 points precision

			header = re.findall(header_regex, value)
			if len(header) > 4:
				cpu_columns = map(lambda x: x.replace('%', ''), header) 

		cpu_dict = dict(zip(cpu_columns, cpu_values))
		
		return cpu_dict

system_info_collector = LinuxSystemCollector()


class ProcessInfoCollector(object):

	def __init__(self):
		memory = system_info_collector.get_memory_info()
		self.total_memory = memory['total_mb']


	def process_list(self):
		stats = subprocess.Popen(['pidstat','-ruht'], 
			stdout=subprocess.PIPE, close_fds=True)\
				.communicate()[0]

		stats_data = stats.splitlines()
		del stats_data[0:2] # Deletes Unix system data

		converted_data = []
		for line in stats_data:
			if re.search('command', line, re.IGNORECASE): # Matches the first line
				header = line.split()
				del header[0] # Deletes the # symbol
			else:
				command = line.split()
				data_dict = dict(zip(header, command))
				
				process_memory_mb = float(self.total_memory/100) * float(data_dict["%MEM"]) # Convert the % in MB
				memory = "{0:.3}".format(process_memory_mb)
				memory = memory.replace(",", ".")

				cpu = "{0:.2f}".format(float(data_dict["%CPU"]))
				cpu = cpu.replace(",", ".")
				
				command = data_dict["Command"]

				if not re.search('_', command, re.IGNORECASE):
					extracted_data = {"cpu": cpu,
								  "memory_mb": memory,
								  "command": command}
					converted_data.append(extracted_data)

		return converted_data
	
process_info_collector = ProcessInfoCollector()
