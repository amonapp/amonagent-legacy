from amonagent.collector import system_info_collector, process_info_collector
from amonagent.settings import settings
from amonagent.utils import unix_utc_now
import sys

class Runner(object):

    def __init__(self):
        self.active_checks = settings.SYSTEM_CHECKS

    def system(self):

        system_info_dict = {}

        now = unix_utc_now()

        if 'memory' in self.active_checks:
            memory = system_info_collector.get_memory_info()

            if memory != False:
                memory['time'] = now
                system_info_dict['memory'] = memory


        if 'cpu' in self.active_checks:
            cpu = system_info_collector.get_cpu_utilization()

            if cpu != False:
                cpu['time'] = now
                system_info_dict['cpu'] = cpu


        if 'loadavg' in self.active_checks:
            loadavg = system_info_collector.get_load_average()

            if loadavg != False:
                loadavg['time'] = now
                system_info_dict['loadavg'] = loadavg


        if 'disk' in self.active_checks:
            disk = system_info_collector.get_disk_usage()

            if disk != False:
                disk['time'] = now
                system_info_dict['disk'] = disk

        if 'network' in self.active_checks and sys.platform != 'darwin':
            network = system_info_collector.get_network_traffic()

            if network != False:
                network['time'] = now
                system_info_dict['network'] = network

        return system_info_dict

    def processes(self):
        now = unix_utc_now()

        process_checks = process_info_collector.process_list()

        process_info_dict = {}
        for process in process_checks:
            command = process["command"]
            del process["command"]
            process_info_dict[command]  = process
            process_info_dict[command]['time'] = now

        return process_info_dict

runner = Runner()



