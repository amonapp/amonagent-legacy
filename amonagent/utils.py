import unicodedata
import re
import calendar
from datetime import datetime


def slugify(string):

	"""
	Slugify a unicode string.

	"""

	return re.sub(r'[-\s]+', '-',
			unicode(
				re.sub(r'[^\w\s-]', '',
					unicodedata.normalize('NFKD', string)
					.encode('ascii', 'ignore'))
				.strip()
				.lower()))


def split_and_slugify(string, separator=":"):
	_string = string.strip().split(separator)
	
	if len(_string) == 2: # Only key, value
		data = {}
		key = slugify(unicode(_string[0]))
		
		try:
			if len(_string[1]) > 0:
				data[key] = str(_string[1].strip())
		except:
			pass

		return data
	
	else:
		return None


# Used in the collector, saves all the data in UTC
def unix_utc_now():
	d = datetime.utcnow()
	_unix = calendar.timegm(d.utctimetuple())

	return _unix