import unittest
from amonagent.remote import Remote
from amonagent.runner import runner
from amonagent.settings import settings
from nose.tools import eq_
import requests
import sys
import amonagent



class TestRemote(unittest.TestCase):

	def setUp(self):
		self.remote = Remote()

	def test_save_system(self):
		system_info = runner.system()
		try:
			r =  requests.get(self.remote.connection_url())
		except:
			r = False

		# Test the API only when the web app is running
		if r != False:
			self.remote.save_system_stats(system_info)

	def test_proxy_url(self):
		eq_(self.remote.connection_url(), 'http://localhost')


