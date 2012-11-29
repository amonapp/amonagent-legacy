import subprocess
import re


memory_stats = subprocess.Popen(['sar','-r' ,'1','1'], 
			stdout=subprocess.PIPE, close_fds=True)\
				.communicate()[0]

memory_data = memory_stats.splitlines()


for line in memory_data:
	if re.search('mem', line):
		header = line.split()
	if re.search('average', line, re.IGNORECASE):
		values = line.split()

header_index = [i for i, item in enumerate(header) if re.search('memfree', item)]
values_index = [i for i, item in enumerate(values) if re.search('\d+', item, re.IGNORECASE)]
header_list = header[header_index[0]:]
values_list = values[values_index[0]:]

if len(header_list) == len(values_list):
	memory_dict = dict(zip(header_list, values_list))
else:
	memory_dict = {}


####################################
stats = subprocess.Popen(['pidstat','-ruh'], 
			stdout=subprocess.PIPE, close_fds=True)\
				.communicate()[0]

#print stats
stats_data = stats.splitlines()
del stats_data[0:2] # Deletes Unix system 

converted_data = []
for line in stats_data:
	if re.search('command', line, re.IGNORECASE):
		header = line.split()
		del header[0] # Deletes the # symbol
	if re.search('\d+', line, re.IGNORECASE):
		command = line.split()
		data_dict = dict(zip(header, command))
		extracted_data = {"cpu": data_dict["%CPU"],
						  "memory": data_dict["%MEM"],
						  "command": data_dict["Command"]}

		print extracted_data

