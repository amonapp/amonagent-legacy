import subprocess
import re

from amonagent.modules.core import get_memory_info

class ProcessesDataCollector(object):

	def __init__(self):
		memory = get_memory_info()
		self.total_memory = memory['total_mb']


	def collect(self):
		stats = subprocess.Popen(['pidstat','-ruhtd'], 
			stdout=subprocess.PIPE, close_fds=True)\
				.communicate()[0]

		stats_data = stats.splitlines()
		del stats_data[0:2] # Deletes Unix system data

		processes_data_dict = {}
		converted_data = []
		for line in stats_data:
			if re.search('command', line, re.IGNORECASE): # Matches the first line
				header = line.split()
				del header[0] # Deletes the # symbol
			else:
				command = line.split()
				data_dict = dict(zip(header, command))
				
				memory_in_percent = data_dict["%MEM"]
				memory_in_percent = memory_in_percent.replace(",", ".")

				process_memory_mb = float(self.total_memory/100) * float(memory_in_percent) # Convert the % in MB
				memory = "{0:.3}".format(process_memory_mb)
				memory = memory.replace(",", ".")

				cpu_percent = data_dict["%CPU"]
				cpu_percent = cpu_percent.replace(",", ".")

				cpu = "{0:.2f}".format(float(cpu_percent))
				cpu = cpu.replace(",", ".")
				
				command = data_dict["Command"]

				kb_write = data_dict.get('kB_wr/s')
				kb_write = kb_write.replace(',', ".")
				
				kb_read = data_dict.get('kB_rd/s')
				kb_read = kb_read.replace(',', ".")

				if not re.search('_', command, re.IGNORECASE):
					extracted_data = {"cpu": cpu,
								  "memory_mb": memory,
								  "kb_read": kb_read,
								  "kb_write": kb_write,
								  "command": command}
					converted_data.append(extracted_data)

		if len(converted_data) > 0:	
			for process in converted_data:
				command = process["command"]
				command = command.replace(".", "")
				del process["command"]
				
				processes_data_dict[command]  = process

		return processes_data_dict
	
processes_data_collector = ProcessesDataCollector()