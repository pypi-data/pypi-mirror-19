import logging
import os
import sys


def configure_logging():
    logging.basicConfig(level=logging.INFO, stream=sys.stderr,
                        format='%(levelname)1.1s - %(name)s: %(message)s')


def require_environment(logger, var_name):
    try:
        return os.environ[var_name]
    except KeyError as exc:
        logger.error('%s is a required environment variable', var_name)
        sys.exit(os.EX_USAGE)
