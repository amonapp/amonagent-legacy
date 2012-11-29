import subprocess
import sys
import re

if sys.platform == 'darwin':
	from amonagent._macos import MacOSSystemCollector
	system_info_collector = MacOSSystemCollector()
else:
	from amonagent._linux import LinuxSystemCollector
	system_info_collector = LinuxSystemCollector()


class ProcessInfoCollector(object):

	def __init__(self):
		memory = system_info_collector.get_memory_info()
		self.total_memory = memory['memtotal']

	def check_process(self, name=None):
		# get the process info, remove grep from the result, print cpu, memory
		# ps aux |grep 'postgres' | grep -v grep | awk '{print $3","$4}' 

		ps = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE, close_fds=True)
		grep = subprocess.Popen(['grep', str(name)], stdin=ps.stdout, stdout=subprocess.PIPE, close_fds=True)
		remove_grep = subprocess.Popen(['grep', '-v','grep'], stdin=grep.stdout, stdout=subprocess.PIPE, close_fds=True)
		awk = subprocess.Popen(['awk', '{print $3","$4}'], stdin=remove_grep.stdout,\
		stdout=subprocess.PIPE, close_fds=True).communicate()[0]	

		lines = [0,0]
		for line in awk.splitlines():
			cpu_memory = line.split(',')
			cpu_memory = map(lambda x:  float(x), cpu_memory)
			lines[0] = lines[0]+cpu_memory[0]
			lines[1] = lines[1]+cpu_memory[1]

		lines  = map(lambda x:  "{0:.2f}".format(x), lines)
		lines = map(lambda x: x.replace(",", "."), lines)
		
		cpu, memory = lines[0], lines[1]

		process_memory_mb = float(self.total_memory/100) * float(memory) # Convert the % in MB
		memory = "{0:.3}".format(process_memory_mb)
		process_info = {'cpu': cpu, 'memory': memory}
		
		return process_info

	def process_list(self):
		stats = subprocess.Popen(['pidstat','-ruh'], 
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

				cpu = "{0:.2f}".format(float(data_dict["%CPU"]))
				cpu = cpu.replace(",", ".")
				
				extracted_data = {"cpu": cpu,
								  "memory": memory,
								  "command": data_dict["Command"]}
				converted_data.append(extracted_data)

		return converted_data
	
process_info_collector = ProcessInfoCollector()

