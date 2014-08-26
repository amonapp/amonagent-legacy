1.8 - 26.08.2014
==============

* Fixed memory leak in the Plugins config reader


1.7 - 21.08.2014
==============

* Stability improvements

1.6
==============

* amonpm - Uninstall method, Install updates the plugins by default

1.5.5
==============

* Fix Memory allocation issue in loadavg

1.5.4
==============

* Fix Debian uninstall script

1.5.3
==============

* Stability bug fixes

1.5.2
==============

* API Check fixes - test using the real server key

1.5.1
==============

* Ignore curl certificate check (--insecure) option

1.5
==============

* Install plugins from the command line - /etc/init.d/amon-agent install mysql
* Security update - the daemon for the agent runs under the amonagent user instead of root


1.3
==============

* Install all available plugins with the agent

1.2
==============

* Fix installation - install both setuptools and pip
* Don't break the agent if the plugin directories doesn't exist (/etc/amoagent/plugins)

1.1
==============

* Information about package updates

1.0.3
==============

* Processes - read/write per second

0.7.5
==============

* Fix locale issues in the process collector module

0.7.4
==============

* Increase the API call timeout to 10 seconds, raise an exception if there is an error

0.7.3
==============

* Remove detailed disk usage collector - too slow on big volumes

0.7.2
==============

* Connection pooling to the API instead of posts - fixes the bug where the agent stops sending information after amon.cx is restarted
* Uptime data

0.7.1
==============

* Improved OS detection (detects Ubuntu, Debian, CentOS, Fedora and Amazon AMI)
* Uptime data

0.7
===============

* Server public IP Address
* Distro info