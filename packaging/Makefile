BUILD=build/package
AGENT=$(BUILD)/amonagent
SRC=../
VERSION=`PYTHONPATH=$(SRC) python -c "from amonagent import __version__; print __version__"`
# VERSION='2.2'

PACKAGES_PATH=/home/martin/amon-packages
DEBIAN_REPO_PATH=$(PACKAGES_PATH)/debian/
RPM_REPO_PATH=$(PACKAGES_PATH)/centos/

PACKAGE="amon-agent"
DEBIAN_PACKAGE_NAME="${PACKAGE}_${VERSION}_all.deb"
CENTOS_PACKAGE_NAME="${PACKAGE}-${VERSION}-1.noarch.rpm"

FPM_BUILD=fpm --epoch 1 -s dir -e -C $(BUILD) \
-a all -m "Amon Packages <packages@amon.cx>" \
--url "http://amon.cx/" \
--description "`cat desc`"\
-v $(VERSION) \
--vendor Amon 

clean:
	rm -rf build

install_repo_base:
	sudo apt-get install reprepro createrepo -y --force-yes


# Layout all of the files common to both versions of the Agent in
# the build directory.
install_base: 
	mkdir -p $(BUILD)
	mkdir -p $(BUILD)/etc/amonagent
	mkdir -p $(BUILD)/etc/amonagent/plugins-enabled
	mkdir -p $(BUILD)/etc/amonagent/plugins
	
	mkdir -p $(BUILD)/var/log/amonagent
	mkdir -p $(BUILD)/usr/bin
	mkdir -p $(BUILD)/var/run/amonagent

	chmod 755 $(BUILD)/var/log/amonagent


	mkdir -p $(BUILD)/etc/init.d
	cp -r $(SRC)/amon-agent $(BUILD)/etc/init.d/amon-agent
	cp -r $(SRC)/amon-agent.py $(BUILD)/usr/bin/amon-agent.py
	cp -r $(SRC)/amonpm $(BUILD)/usr/bin/amonpm
	find $(BUILD)/etc/amonagent/ -type f -name "*.pyc" -exec rm -f {} \;
	chmod 755 $(BUILD)/etc/init.d/amon-agent

	@echo $(VERSION)



# =====================
# Ubuntu/Debian
# =====================
build_deb: clean install_base
	rm -f *.deb
	FPM_EDITOR="echo 'Replaces: amon-agent (<= $(VERSION))' >>" \
$(FPM_BUILD) -t deb \
-n amon-agent \
-d "python (>= 2.6)" \
-d "curl" \
-d "adduser" \
-d "sysstat" \
-d "git" \
--post-install debian/postinst \
--post-uninstall debian/postrm \
--pre-uninstall  debian/prerm \
.
	

# =====================
# CentOS/Fedora
# =====================
build_rpm: clean install_base
	rm -f *.rpm
	FPM_EDITOR="echo ''>>"  \
$(FPM_BUILD) -t rpm \
-n "amon-agent" \
-d "curl" \
-d "sysstat" \
-d "git" \
--conflicts "amon-agent < $(VERSION)" \
--post-install	   rpm/postinst \
--pre-uninstall	   rpm/prerm \
--post-uninstall   rpm/postrm \
.
	

update_debian_repo:
	cp "amon-agent_$(VERSION)_all.deb" $(DEBIAN_REPO_PATH)
	find $(DEBIAN_REPO_PATH)  -name \*.deb -exec reprepro --ask-passphrase -Vb $(DEBIAN_REPO_PATH)repo includedeb amon {} \;

update_rpm_repo:
	cp "amon-agent-$(VERSION)-1.noarch.rpm" $(RPM_REPO_PATH)
	createrepo --update $(RPM_REPO_PATH)


deploy: update_debian_repo update_rpm_repo
	sudo ntpdate time.nist.gov
	python s3uploader.py

all: clean amon_agent_deb amon_agent_rpm


build_arm_base:
	cp debian/Dockerfile.arm.base Dockerfile
	docker build --force-rm=true --rm=true --no-cache -t=martinrusev/amonbase-arm .  
	rm Dockerfile

build_arm:
	cp debian/Dockerfile.arm Dockerfile
	docker build --rm=true --no-cache . 
	rm Dockerfile


test_arm:
	cp debian/Dockerfile.arm Dockerfile
	sed -i s/AMON_DEB_FILE/"$(DEBIAN_PACKAGE_NAME)"/g Dockerfile
	docker build --rm=true --no-cache . 
	rm Dockerfile

test_debian:
	cp debian/Dockerfile Dockerfile
	sed -i s/AMON_DEB_FILE/"$(DEBIAN_PACKAGE_NAME)"/g Dockerfile
	docker build --rm=true --no-cache . 
	rm Dockerfile



test_rpm:
	cp rpm/Dockerfile Dockerfile
	sed -i s/AMON_RPM_FILE/"$(CENTOS_PACKAGE_NAME)"/g Dockerfile
	docker build --rm=true --no-cache . 
	rm Dockerfile

test_all: test_debian test_rpm


test_debian_repo:
	cp debian/Dockerfile.repo Dockerfile
	docker build --rm=true --no-cache . 
	rm Dockerfile

test_debian_repo_arm:
	cp debian/Dockerfile.repo Dockerfile
	docker build --rm=true --no-cache . 
	rm Dockerfile


test_rpm_repo:
	cp rpm/Dockerfile.repo Dockerfile
	cp rpm/amon.repo amon.repo
	docker build --rm=true --no-cache .
	rm Dockerfile
	rm amon.repo

test_debian_install_script:
	cp debian/Dockerfile.install Dockerfile
	docker build --rm=true --no-cache .
	rm Dockerfile

test_rpm_install_script:
	cp rpm/Dockerfile.install Dockerfile
	docker build --rm=true --no-cache .
	rm Dockerfile