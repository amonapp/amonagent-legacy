import logging
from amonagent.settings import settings

# Configure logging
logging.basicConfig(filename=settings.LOGFILE, level=logging.ERROR,
	format="%(asctime)s|  %(filename)s:%(lineno)d | %(message)s")
log = logging.getLogger('amonagent')