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