import shelve
import sys
sys.path.insert(0,'/home/martin/amonagent')
from amonagent.runner import runner

class Cache(object):

    def __init__(self):
        self.cache = shelve.open('/home/martin/amonagent.cache')

    def store(self, data, type=None):
        index_type = 'system' if type == 'system' else 'process'

        try:
            index = self.cache[index_type]
        except:
            index = 0
            self.cache[index_type] = index

        element_key = "{0}-{1}".format(index_type, index)
        self.cache[element_key] = data

        self.cache[index_type] = index+1

cache = Cache()
data = runner.system()
cache.store(data, 'system')

