import logging
import sys

FORMAT = '%(asctime)s : %(message)s'
logging.basicConfig(
    format=FORMAT,
    stream=sys.stdout,
)
logger = logging.getLogger()
logger.setLevel('INFO')
