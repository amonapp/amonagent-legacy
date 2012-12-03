from amonagent.collector import system_info_collector, process_info_collector
from amonagent.settings import settings
from amonagent.utils import unix_utc_now
import sys

class Runner(object):

    def system(self):

        system_info_dict = {}

        memory = system_info_collector.get_memory_info()
        cpu = system_info_collector.get_cpu_utilization()
        loadavg = system_info_collector.get_load_average()
        disk = system_info_collector.get_disk_usage()
        network = system_info_collector.get_network_traffic()

        if memory != False:
            system_info_dict['memory'] = memory

        if cpu != False:
            system_info_dict['cpu'] = cpu

        if loadavg != False:
            system_info_dict['loadavg'] = loadavg

        if disk != False: 
            system_info_dict['disk'] = disk

        if network != False:
            system_info_dict['network'] = network


        return system_info_dict

    def processes(self):

        process_checks = process_info_collector.process_list()

        process_info_dict = {}
        for process in process_checks:
            command = process["command"]
            del process["command"]
            process_info_dict[command]  = process

        return process_info_dict

    def plugins(self):
        loaded_plugins = settings.PLUGINS
        plugins_dict = {}
        if loaded_plugins:
            for plugin in loaded_plugins.keys():
                if plugin == 'apache':
                    apache = __import__("amonagent.plugins.apache" ,globals(), locals(), 'plugin')
                    plugins_dict['apache'] = apache.plugin.build_report()
                if plugin == 'nginx':
                    nginx = __import__("amonagent.plugins.nginx" ,globals(), locals(), 'plugin')
                    plugins_dict['nginx'] = nginx.plugin.build_report()

        return plugins_dict
                   


    def distribution_info(self):
        distribution_info = system_info_collector.get_distro_info()
        distribution_info['plugins'] = settings.PLUGINS.keys()

        return distribution_info


runner = Runner()



