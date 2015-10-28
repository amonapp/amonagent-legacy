## Installing the amon-agent with Ansible

- Copy all the files from deployment/ansible to a local path
- In amon-agent.yml, replace the following variables with the appropriate values:

```
	api_key - a valid API key 
	amon_instance - the IP or domain pointing to your Amon instance

```

## Running the playbook 



```
ansible-playbook amon-agent.yml

```

Tested on Debian/Ubuntu and CentOS