from amonagent.modules.distro import get_distro

class TestGetDistro(object):

	def test_get_distro(self):
		result = get_distro()

		assert isinstance(result, dict)
		assert 'release' in result
		assert 'id' in result
		assert 'type' in result


