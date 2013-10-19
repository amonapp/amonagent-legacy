from nose.tools import eq_
import requests
from amonagent.utils.helpers import slugify
from amonagent.plugins.apache import AmonApachePlugin

class TestApachePlugin(object):
	

	def test_build_report(self):
		apache = AmonApachePlugin()

		report = apache.build_report()
		 
		white_list = ['reqpersec','busyworkers','idleworkers','bytespersec']
		for key, value in report.items():
			assert key in white_list
			assert isinstance(value, float)