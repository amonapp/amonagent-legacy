from amonagent.modules.packages import system_packages

class TestGetPackagesForUpdate(object):

	def test_get_distro(self):
		result = system_packages.result()

		for value in result:
			assert 'current_version' in value.keys()
			assert 'new_version' in value.keys()
			assert 'name' in value.keys()