# (c) 2012, Michael DeHaan <michael.dehaan@gmail.com>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

import os
import stat
import array
import errno
import fcntl
import fnmatch
import glob
import platform
import re
import signal
import socket
import struct
import datetime
import getpass
import pwd
import ConfigParser
import StringIO

from string import maketrans

try:
    import json
except ImportError:
    import simplejson as json

# --------------------------------------------------------------
# timeout function to make sure some fact gathering
# steps do not exceed a time limit


# --------------------------------------------------------------
def get_file_content(path, default=None, strip=True):
    data = default
    if os.path.exists(path) and os.access(path, os.R_OK):
        try:
            datafile = open(path)
            data = datafile.read()
            if strip:
                data = data.strip()
            if len(data) == 0:
                data = default
        finally:
            datafile.close()
    return data
    
class Facts(object):
    """
    This class should only attempt to populate those facts that
    are mostly generic to all systems.  This includes platform facts,
    service facts (e.g. ssh keys or selinux), and distribution facts.
    Anything that requires extensive code or may have more than one
    possible implementation to establish facts for a given topic should
    subclass Facts.
    """

    # i86pc is a Solaris and derivatives-ism
    _I386RE = re.compile(r'i([3456]86|86pc)')
    # For the most part, we assume that platform.dist() will tell the truth.
    # This is the fallback to handle unknowns or exceptions
    OSDIST_LIST = ( ('/etc/oracle-release', 'Oracle Linux'),
                    ('/etc/redhat-release', 'RedHat'),
                    ('/etc/vmware-release', 'VMwareESX'),
                    ('/etc/openwrt_release', 'OpenWrt'),
                    ('/etc/system-release', 'OtherLinux'),
                    ('/etc/alpine-release', 'Alpine'),
                    ('/etc/release', 'Solaris'),
                    ('/etc/arch-release', 'Archlinux'),
                    ('/etc/SuSE-release', 'SuSE'),
                    ('/etc/os-release', 'SuSE'),
                    ('/etc/gentoo-release', 'Gentoo'),
                    ('/etc/os-release', 'Debian'),
                    ('/etc/lsb-release', 'Mandriva') )
    SELINUX_MODE_DICT = { 1: 'enforcing', 0: 'permissive', -1: 'disabled' }

    # A list of dicts.  If there is a platform with more than one
    # package manager, put the preferred one last.  If there is an
    # ansible module, use that as the value for the 'name' key.
    PKG_MGRS = [ { 'path' : '/usr/bin/yum',         'name' : 'yum' },
                 { 'path' : '/usr/bin/apt-get',     'name' : 'apt' },
                 { 'path' : '/usr/bin/zypper',      'name' : 'zypper' },
                 { 'path' : '/usr/sbin/urpmi',      'name' : 'urpmi' },
                 { 'path' : '/usr/bin/pacman',      'name' : 'pacman' },
                 { 'path' : '/bin/opkg',            'name' : 'opkg' },
                 { 'path' : '/opt/local/bin/pkgin', 'name' : 'pkgin' },
                 { 'path' : '/opt/local/bin/port',  'name' : 'macports' },
                 { 'path' : '/sbin/apk',            'name' : 'apk' },
                 { 'path' : '/usr/sbin/pkg',        'name' : 'pkgng' },
                 { 'path' : '/usr/sbin/swlist',     'name' : 'SD-UX' },
                 { 'path' : '/usr/bin/emerge',      'name' : 'portage' },
                 { 'path' : '/usr/sbin/pkgadd',     'name' : 'svr4pkg' },
                 { 'path' : '/usr/bin/pkg',         'name' : 'pkg' },
    ]

    def __init__(self, load_on_init=True):

        self.facts = {}

        if load_on_init:
            self.get_platform_facts()
            self.get_distribution_facts()


    def populate(self):
        return self.facts

    # Platform
    # platform.system() can be Linux, Darwin, Java, or Windows
    def get_platform_facts(self):
        self.facts['system'] = platform.system()
        self.facts['kernel'] = platform.release()
        self.facts['machine'] = platform.machine()
        self.facts['python_version'] = platform.python_version()
        self.facts['fqdn'] = socket.getfqdn()
        self.facts['hostname'] = platform.node().split('.')[0]
        self.facts['nodename'] = platform.node()
        self.facts['domain'] = '.'.join(self.facts['fqdn'].split('.')[1:])
        arch_bits = platform.architecture()[0]
        self.facts['userspace_bits'] = arch_bits.replace('bit', '')
        if self.facts['machine'] == 'x86_64':
            self.facts['architecture'] = self.facts['machine']
            if self.facts['userspace_bits'] == '64':
                self.facts['userspace_architecture'] = 'x86_64'
            elif self.facts['userspace_bits'] == '32':
                self.facts['userspace_architecture'] = 'i386'
        elif Facts._I386RE.search(self.facts['machine']):
            self.facts['architecture'] = 'i386'
            if self.facts['userspace_bits'] == '64':
                self.facts['userspace_architecture'] = 'x86_64'
            elif self.facts['userspace_bits'] == '32':
                self.facts['userspace_architecture'] = 'i386'
        else:
            self.facts['architecture'] = self.facts['machine']
        if self.facts['system'] == 'Linux':
            self.get_distribution_facts()
        elif self.facts['system'] == 'AIX':
            rc, out, err = module.run_command("/usr/sbin/bootinfo -p")
            data = out.split('\n')
            self.facts['architecture'] = data[0]
        elif self.facts['system'] == 'OpenBSD':
            self.facts['architecture'] = platform.uname()[5]




    # platform.dist() is deprecated in 2.6
    # in 2.6 and newer, you should use platform.linux_distribution()
    def get_distribution_facts(self):

        # A list with OS Family members
        OS_FAMILY = dict(
            RedHat = 'RedHat', Fedora = 'RedHat', CentOS = 'RedHat', Scientific = 'RedHat',
            SLC = 'RedHat', Ascendos = 'RedHat', CloudLinux = 'RedHat', PSBM = 'RedHat',
            OracleLinux = 'RedHat', OVS = 'RedHat', OEL = 'RedHat', Amazon = 'RedHat',
            XenServer = 'RedHat', Ubuntu = 'Debian', Debian = 'Debian', Raspbian = 'Debian', SLES = 'Suse',
            SLED = 'Suse', openSUSE = 'Suse', SuSE = 'Suse', Gentoo = 'Gentoo', Funtoo = 'Gentoo',
            Archlinux = 'Archlinux', Mandriva = 'Mandrake', Mandrake = 'Mandrake',
            Solaris = 'Solaris', Nexenta = 'Solaris', OmniOS = 'Solaris', OpenIndiana = 'Solaris',
            SmartOS = 'Solaris', AIX = 'AIX', Alpine = 'Alpine', MacOSX = 'Darwin',
            FreeBSD = 'FreeBSD', HPUX = 'HP-UX'
        )

        # TODO: Rewrite this to use the function references in a dict pattern
        # as it's much cleaner than this massive if-else
        if self.facts['system'] == 'AIX':
            self.facts['distribution'] = 'AIX'
            rc, out, err = module.run_command("/usr/bin/oslevel")
            data = out.split('.')
            self.facts['distribution_version'] = data[0]
            self.facts['distribution_release'] = data[1]
        elif self.facts['system'] == 'HP-UX':
            self.facts['distribution'] = 'HP-UX'
            rc, out, err = module.run_command("/usr/sbin/swlist |egrep 'HPUX.*OE.*[AB].[0-9]+\.[0-9]+'", use_unsafe_shell=True)
            data = re.search('HPUX.*OE.*([AB].[0-9]+\.[0-9]+)\.([0-9]+).*', out)
            if data:
                self.facts['distribution_version'] = data.groups()[0]
                self.facts['distribution_release'] = data.groups()[1]
        elif self.facts['system'] == 'Darwin':
            self.facts['distribution'] = 'MacOSX'
            rc, out, err = module.run_command("/usr/bin/sw_vers -productVersion")
            data = out.split()[-1]
            self.facts['distribution_version'] = data
        elif self.facts['system'] == 'FreeBSD':
            self.facts['distribution'] = 'FreeBSD'
            self.facts['distribution_release'] = platform.release()
            self.facts['distribution_version'] = platform.version()
        elif self.facts['system'] == 'OpenBSD':
            self.facts['distribution'] = 'OpenBSD'
            self.facts['distribution_release'] = platform.release()
            rc, out, err = module.run_command("/sbin/sysctl -n kern.version")
            match = re.match('OpenBSD\s[0-9]+.[0-9]+-(\S+)\s.*', out)
            if match:
                self.facts['distribution_version'] = match.groups()[0]
            else:
                self.facts['distribution_version'] = 'release'
        else:
            dist = platform.dist()
            self.facts['distribution'] = dist[0].capitalize() or 'NA'
            self.facts['distribution_version'] = dist[1] or 'NA'
            self.facts['distribution_major_version'] = dist[1].split('.')[0] or 'NA'
            self.facts['distribution_release'] = dist[2] or 'NA'
            # Try to handle the exceptions now ...
            for (path, name) in Facts.OSDIST_LIST:
                if os.path.exists(path):
                    if os.path.getsize(path) > 0:
                        if self.facts['distribution'] in ('Fedora', ):
                            # Once we determine the value is one of these distros
                            # we trust the values are always correct
                            break
                        elif name == 'Oracle Linux':
                            data = get_file_content(path)
                            if 'Oracle Linux' in data:
                                self.facts['distribution'] = name
                            else:
                                self.facts['distribution'] = data.split()[0]
                            break
                        elif name == 'RedHat':
                            data = get_file_content(path)
                            if 'Red Hat' in data:
                                self.facts['distribution'] = name
                            else:
                                self.facts['distribution'] = data.split()[0]
                            break
                        elif name == 'OtherLinux':
                            data = get_file_content(path)
                            if 'Amazon' in data:
                                self.facts['distribution'] = 'Amazon'
                                self.facts['distribution_version'] = data.split()[-1]
                                break
                        elif name == 'OpenWrt':
                            data = get_file_content(path)
                            if 'OpenWrt' in data:
                                self.facts['distribution'] = name
                                version = re.search('DISTRIB_RELEASE="(.*)"', data)
                                if version:
                                    self.facts['distribution_version'] = version.groups()[0]
                                release = re.search('DISTRIB_CODENAME="(.*)"', data)
                                if release:
                                    self.facts['distribution_release'] = release.groups()[0]
                                break
                        elif name == 'Alpine':
                            data = get_file_content(path)
                            self.facts['distribution'] = name
                            self.facts['distribution_version'] = data
                            break
                        elif name == 'Solaris':
                            data = get_file_content(path).split('\n')[0]
                            if 'Solaris' in data:
                                ora_prefix = ''
                                if 'Oracle Solaris' in data:
                                    data = data.replace('Oracle ','')
                                    ora_prefix = 'Oracle '
                                self.facts['distribution'] = data.split()[0]
                                self.facts['distribution_version'] = data.split()[1]
                                self.facts['distribution_release'] = ora_prefix + data
                                break

                            uname_rc, uname_out, uname_err = module.run_command(['uname', '-v'])
                            distribution_version = None
                            if 'SmartOS' in data:
                                self.facts['distribution'] = 'SmartOS'
                                if os.path.exists('/etc/product'):
                                    product_data = dict([l.split(': ', 1) for l in get_file_content('/etc/product').split('\n') if ': ' in l])
                                    if 'Image' in product_data:
                                        distribution_version = product_data.get('Image').split()[-1]
                            elif 'OpenIndiana' in data:
                                self.facts['distribution'] = 'OpenIndiana'
                            elif 'OmniOS' in data:
                                self.facts['distribution'] = 'OmniOS'
                                distribution_version = data.split()[-1]
                            elif uname_rc == 0 and 'NexentaOS_' in uname_out:
                                self.facts['distribution'] = 'Nexenta'
                                distribution_version = data.split()[-1].lstrip('v')

                            if self.facts['distribution'] in ('SmartOS', 'OpenIndiana', 'OmniOS', 'Nexenta'):
                                self.facts['distribution_release'] = data.strip()
                                if distribution_version is not None:
                                    self.facts['distribution_version'] = distribution_version
                                elif uname_rc == 0:
                                    self.facts['distribution_version'] = uname_out.split('\n')[0].strip()
                                break

                        elif name == 'SuSE':
                            data = get_file_content(path)
                            if 'suse' in data.lower():
                                if path == '/etc/os-release':
                                    for line in data.splitlines():
                                        distribution = re.search("^NAME=(.*)", line)
                                        if distribution:
                                            self.facts['distribution'] = distribution.group(1).strip('"')
                                        distribution_version = re.search('^VERSION_ID="?([0-9]+\.?[0-9]*)"?', line) # example pattern are 13.04 13.0 13
                                        if distribution_version:
                                             self.facts['distribution_version'] = distribution_version.group(1)
                                        if 'open' in data.lower():
                                            release = re.search("^PRETTY_NAME=[^(]+ \(?([^)]+?)\)", line)
                                            if release:
                                                self.facts['distribution_release'] = release.groups()[0]
                                        elif 'enterprise' in data.lower():
                                             release = re.search('^VERSION_ID="?[0-9]+\.?([0-9]*)"?', line) # SLES doesn't got funny release names
                                             if release:
                                                 release = release.group(1)
                                             else:
                                                 release = "0" # no minor number, so it is the first release
                                             self.facts['distribution_release'] = release
                                    break
                                elif path == '/etc/SuSE-release':
                                    if 'open' in data.lower():
                                        data = data.splitlines()
                                        distdata = get_file_content(path).split('\n')[0]
                                        self.facts['distribution'] = distdata.split()[0]
                                        for line in data:
                                            release = re.search('CODENAME *= *([^\n]+)', line)
                                            if release:
                                                self.facts['distribution_release'] = release.groups()[0].strip()
                                    elif 'enterprise' in data.lower():
                                        lines = data.splitlines()
                                        distribution = lines[0].split()[0]
                                        if "Server" in data:
                                            self.facts['distribution'] = "SLES"
                                        elif "Desktop" in data:
                                            self.facts['distribution'] = "SLED"
                                        for line in lines:
                                            release = re.search('PATCHLEVEL = ([0-9]+)', line) # SLES doesn't got funny release names
                                            if release:
                                                self.facts['distribution_release'] = release.group(1)
                                                self.facts['distribution_version'] = self.facts['distribution_version'] + '.' + release.group(1)
                        elif name == 'Debian':
                            data = get_file_content(path)
                            if 'Debian' in data or 'Raspbian' in data:
                                release = re.search("PRETTY_NAME=[^(]+ \(?([^)]+?)\)", data)
                                if release:
                                    self.facts['distribution_release'] = release.groups()[0]
                                break
                        elif name == 'Mandriva':
                            data = get_file_content(path)
                            if 'Mandriva' in data:
                                version = re.search('DISTRIB_RELEASE="(.*)"', data)
                                if version:
                                    self.facts['distribution_version'] = version.groups()[0]
                                release = re.search('DISTRIB_CODENAME="(.*)"', data)
                                if release:
                                    self.facts['distribution_release'] = release.groups()[0]
                                self.facts['distribution'] = name
                                break
                    else:
                        self.facts['distribution'] = name
        machine_id = get_file_content("/var/lib/dbus/machine-id") or get_file_content("/etc/machine-id")
        if machine_id:
            machine_id = machine_id.split('\n')[0]
            self.facts["machine_id"] = machine_id
        self.facts['os_family'] = self.facts['distribution']
        if self.facts['distribution'] in OS_FAMILY:
            self.facts['os_family'] = OS_FAMILY[self.facts['distribution']]



def get_distro():
	distro = {}
	f = Facts(load_on_init=False)
	f.get_platform_facts()
	f.get_distribution_facts()

	facts_filter = [
		'distribution_version', 
		'distribution',
	]
	replaced_names = {
		'distribution_version': 'version',
		'distribution' : 'name'
	}
	for key, fact in f.facts.items():
		if key in facts_filter:
			reported_key = replaced_names[key]
			distro[reported_key] = fact
			

	return distro

print get_distro()