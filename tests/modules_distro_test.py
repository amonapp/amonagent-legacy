from amonagent.modules.distro import get_distro, parse_distro_file

class TestGetDistro(object):

	def test_get_distro(self):
		result = get_distro()

		assert isinstance(result, dict)
		assert 'release' in result
		assert 'id' in result
		assert 'type' in result


	# def test_parse_distro_file(self):

	# 	centos = ["CentOS Linux release 7.0.1406 (Core)"]

	# 	assert False