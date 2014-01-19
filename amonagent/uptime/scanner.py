import subprocess
import xmltodict

class AmonUptimeScanner(object):
	
	def __init__(self, host = None):
		self.host = host
		self.result = None

	def _parse_nmap_xml(self, xml_string):
		report_list = []

		tree = xmltodict.parse(xml_string)
		
		result = tree['nmaprun']['host']
		
		ports= result['ports']['port']

		for port in ports:
			port_id = port.get("@portid", None)

			state = port['state']
			service = port['service']

			if port_id:
				current_state = state.get('@state', None)
				
				if current_state:
					current_state = 1 if current_state == 'open' else 0 

				result = {
					"protocol": port.get("@protocol", None), 
					"port" : int(port_id), 
					"state": current_state, 
					"state_reason": state.get('@reason', None), 
					"name": service.get('@name', None)
				}

				report_list.append(result)
		
		return report_list

	def scan_results(self):
		result = False
		
		# -oX - output XML
		# -sT - stealth scan, don't ping
		# -d3 - logging level
		# -p0 - disable nmap ping
		# -n  - Never do DNS resolution
		args = ['nmap', '-sT', '-P0', '-n', '-oX', '-']  + [self.host]
		
		popen_result = subprocess.Popen(args, bufsize=100000, 
			stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


		(report_xml, nmap_err) = popen_result.communicate()


		if len(nmap_err) == 0:
			result = self._parse_nmap_xml(report_xml)
		

		return result 





uptime_scanner = AmonUptimeScanner(host='127.0.0.1')
