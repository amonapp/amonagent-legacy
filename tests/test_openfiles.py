import __builtin__
openfiles = set()
oldfile = __builtin__.file

from amonagent.check import test_checks, test_plugins
from amonagent.modules.plugins import discover_plugins


class newfile(oldfile):
	def __init__(self, *args):
		self.x = args[0]
		print "### OPENING %s ###" % str(self.x)            
		oldfile.__init__(self, *args)
		openfiles.add(self)

	def close(self):
		print "### CLOSING %s ###" % str(self.x)
		oldfile.close(self)
		openfiles.remove(self)
oldopen = __builtin__.open


def newopen(*args):
	return newfile(*args)
__builtin__.file = newfile
__builtin__.open = newopen

def test_open_files():
	test_checks()
	test_plugins()
	discover_plugins()


	print "### %d OPEN FILES: [%s]" % (len(openfiles), ", ".join(f.x for f in openfiles))

	assert len(openfiles) == 0

