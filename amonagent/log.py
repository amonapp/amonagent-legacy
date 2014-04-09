import logging
import logging.handlers
import os
import sys
import traceback

from amonagent.settings import settings

def get_log_date_format():
	return "%Y-%m-%d %H:%M:%S %Z"

def get_log_format(logger_name):
	 return '%%(asctime)s | %%(levelname)s | %s | %%(name)s(%%(filename)s:%%(lineno)s) | %%(message)s' % logger_name


def initialize_logging(logger_name):

	log_file = settings.LOGFILE

	logging_config = {
		'filename': log_file,
		'level': logging.ERROR,
	}
	try:

		logging.basicConfig(
			format=get_log_format(logger_name),
			level=logging_config['level'],
		)


		if log_file:
			# make sure the log directory is writeable
			# NOTE: the entire directory needs to be writable so that rotation works
			if os.access(os.path.dirname(log_file), os.R_OK | os.W_OK):
				file_handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=settings.LOGGING_MAX_BYTES, backupCount=1)
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

	global log
	log = logging.getLogger(__name__)