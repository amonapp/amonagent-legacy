# Create/check server key
{% set api_key = "valid_api_key" %}
{% set amon_instance = "http://youramoninstance" %}
{{amon_instance}}/api/v1/servers/create/?api_key={{api_key}}&key={{grains['machine_id']}}&name={{grains['nodename']}}:
  http.query:
    - status: 200
    - method: GET


amon-agent:
  {% if grains['os_family'] != 'Windows' %}
  pkgrepo.managed:
    - humanname: Amon Agent Repository
    {% if grains['os_family'] == 'Debian' %}
    - name: deb http://packages.amon.cx/repo amon contrib
    - file: /etc/apt/sources.list.d/amonagent.list
    - keyid: AD53961F
    - keyserver: keyserver.ubuntu.com
    {% elif grains['os_family'] == 'RedHat' %}
    - baseurl: priority=1
    - gpgcheck: 0
    - enabled: 1
    {% endif %}
    - require_in:
      - pkg: amon-agent
  {% endif %}
  pkg:
    - installed


/etc/amon-agent.conf:
  file.managed:
    - source: salt://amon-agent/amon-agent.conf
    - template: jinja
    - user: root
    - group: root
    - mode: 644


amon-agent-running:
  service.running:
    - name: amon-agent
    - enable: True
    - watch:
      - pkg: amon-agent


amon_agent_restart: 
  cmd.run:
    - name: /etc/init.d/amon-agent restart 
