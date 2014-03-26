BUILD=build/package
AGENT=$(BUILD)/amonagent
SRC=../
VERSION=`PYTHONPATH=$(SRC) python -c "from amonagent import __version__; print __version__"`

FPM_BUILD=fpm --epoch 1 -s dir -e -C $(BUILD) \
-a all -m "Amon Packages <packages@amon.cx>" \
--url "http://amon.cx/" \
--description "`cat desc`"\
-v $(VERSION) \
--vendor Amon 

clean:
	rm -rf build
	rm -f *.deb *.rpm


# Layout all of the files common to both versions of the Agent in
# the build directory.
install_base: 
	mkdir -p $(BUILD)
	mkdir -p $(BUILD)/etc/amonagent
	mkdir -p $(BUILD)/etc/amonagent/plugins-enabled
	mkdir -p $(BUILD)/etc/amonagent/plugins
	mkdir -p $(BUILD)/var/log/amonagent

	chmod 755 $(BUILD)/var/log/amonagent


	mkdir -p $(BUILD)/etc/init.d
	cp -r $(SRC)/amon-agent $(BUILD)/etc/init.d/amon-agent
	cp -r $(SRC)/amon-agent.conf $(BUILD)/etc/amon-agent.conf
	chmod 755 $(BUILD)/etc/init.d/amon-agent

	@echo $(VERSION)



# =====================
# Ubuntu/Debian
# =====================
amon_agent_deb: clean install_base
	FPM_EDITOR="echo 'Replaces: amon-agent (<= $(VERSION))' >>" \
$(FPM_BUILD) -t deb \
-n amon-agent \
-d "python (>= 2.6)" \
-d "python-dev" \
-d "python-setuptools" \
-d "adduser" \
-d "sysstat" \
--post-install debian/postinst \
--post-uninstall debian/postrm \
--pre-uninstall  debian/prerm \
.

# =====================
# CentOS/Fedora
# =====================
amon_agent_rpm: clean install_base
	FPM_EDITOR="echo ''>>"  \
$(FPM_BUILD) -t rpm \
-n "amon-agent" \
-d "python-devel" \
-d "python-setuptools" \
-d "sysstat" \
--conflicts "amon-agent < $(VERSION)" \
--pre-install	   rpm/preinst \
--post-install	   rpm/postinst \
--pre-uninstall	   rpm/prerm \
--post-uninstall   rpm/postrm \
.

all: clean amon_agent_deb amon_agent_rpm


test_debian:
	cp debian/Dockerfile Dockerfile
	docker build . 
	rm Dockerfile


test_rpm:
	cp rpm/Dockerfile Dockerfile
	docker build . 
	rm Dockerfile