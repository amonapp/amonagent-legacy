# Amon agent packaging



## Requirements

	fpm, docker 


Docker images:

	docker pull ubuntu

	docker pull centos


## Usage 

	make all # Compiles CentOS and Debian packages 


## Testing 

	make test_debian # Copies the Dockerfile from debian/Dockerfile and runs it 
	make test_rpm # Copies the Dockerfile from rpm/Dockerfile and runs it 


	# Test packages.amon.cx 
	make test_debian_repo
	make test_rpm_repo


## Add files to the Debian repo

	find  -name \*.deb -exec reprepro --ask-passphrase -Vb repo includedeb amon {} \;