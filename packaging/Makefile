BUILD=build/package
AGENT=$(BUILD)/amonagent
SRC=../
VERSION=`PYTHONPATH=$(SRC) python -c "from amonagent import __version__; print __version__"`

FPM_BUILD=fpm --epoch 1 -s dir -e -C $(BUILD) \
-a all -m "Amon Packages <package@amon.cx>" \
--url "http://amon.cx/" \
--description "`cat desc`"\
-v $(VERSION) \
--vendor Amon 

clean:
	rm -rf build
	rm -f *.deb *.rpm


# Copy the code to our root directory.
source:
	mkdir -p $(AGENT)
	cp -r $(SRC)/amonagent $(AGENT)/
	cp -r $(SRC)/*.py $(AGENT)/
	cp -r $(SRC)/requirements.txt $(AGENT)/
	cp -r $(SRC)/MANIFEST.in $(AGENT)/
	find $(AGENT) -name "*.pyc" -exec rm {} \;



# Layout all of the files common to both versions of the Agent in
# the build directory.
install_base: source
	mkdir -p $(BUILD)
	mkdir -p $(BUILD)/etc/amonagent
	mkdir -p $(BUILD)/etc/amonagent/plugins-enabled
	mkdir -p $(BUILD)/etc/amonagent/plugins
	mkdir -p $(BUILD)/var/log/amonagent

	chmod 755 $(BUILD)/var/log/amonagent



# =====================
# DEBIAN
# =====================

install_deb: install_base
	mkdir -p $(BUILD)/etc/init.d
	cp -r $(SRC)/amon-agent $(BUILD)/etc/init.d/amon-agent
	chmod 755 $(BUILD)/etc/init.d/amon-agent
	python $(AGENT)/setup.py install
	@echo $(VERSION)


amon_agent_deb: clean install_deb
	FPM_EDITOR="echo 'Replaces: amon-agent (<= $(VERSION))' >>" \
$(FPM_BUILD) -t deb \
-n amon-agent \
-d "python (>= 2.6)" \
-d "python-dev" \
-d "python-setuptools" \
-d "adduser" \
-d "sysstat" \
--pre-install debian/preinst \
--post-install debian/postinst \
--post-uninstall debian/postrm \
--pre-uninstall  debian/prerm \
.


all: clean deb rpm