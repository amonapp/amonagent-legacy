import logging
import logging.handlers
import os
import sys
import traceback

from amonagent.settings import settings

LOGGING_MAX_BYTES = 5 * 1024 * 1024

log = logging.getLogger(__name__)


def get_log_date_format():
	return "%Y-%m-%d %H:%M:%S %Z"

def get_log_format(logger_name):
	 return '%%(asctime)s | %%(levelname)s | dd.%s | %%(name)s(%%(filename)s:%%(lineno)s) | %%(message)s' % logger_name

	 
def initialize_logging(logger_name):

	logging_config = {
		'filename': settings.LOGFILE,
		'level': logging.ERROR,
	}
	try:

		logging.basicConfig(
			format=get_log_format(logger_name),
			level=logging_config['level'] or logging.INFO,
		)



		log_file = logging_config.get('filename')

		if log_file:
			# make sure the log directory is writeable
			# NOTE: the entire directory needs to be writable so that rotation works
			if os.access(os.path.dirname(log_file), os.R_OK | os.W_OK):
				file_handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=LOGGING_MAX_BYTES, backupCount=1)
				formatter = logging.Formatter(get_log_format(logger_name), get_log_date_format())
				file_handler.setFormatter(formatter)

				root_log = logging.getLogger()
				root_log.addHandler(file_handler)
			else:
				sys.stderr.write("Log file is unwritable: '%s'\n" % log_file)

	except Exception, e:
		sys.stderr.write("Couldn't initialize logging: %s\n" % str(e))
		traceback.print_exc()

		# if config fails entirely, enable basic stdout logging as a fallback
		logging.basicConfig(
			format=get_log_format(logger_name),
			level=logging.INFO,
		)

	# re-get the log after logging is initialized
	global log
	log = logging.getLogger(__name__)