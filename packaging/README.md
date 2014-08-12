# Amon agent packaging



## Requirements

	fpm, docker 


Docker images:

	docker pull martinrusev/amonbase

	docker pull martinrusev/centos


## Usage 

	make all # Compiles CentOS and Debian packages and uploads to S3


## Testing 

	make test_debian # Copies the Dockerfile from debian/Dockerfile and runs it 
	make test_rpm # Copies the Dockerfile from rpm/Dockerfile and runs it 


	# Test packages.amon.cx 
	make test_debian_repo
	make test_rpm_repo