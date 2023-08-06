import logging
import json
import os
import pathlib
import sys

import maya
import requests
from ictools import auth, cli


_logger = logging.getLogger(__name__)


class Connection(object):

    def __init__(self, api_token):
        self.logger = _logger.getChild('Connection')
        self.auth = auth.HTTPTokenAuth(api_token)
        self.session = requests.Session()
        self.headers = {'Accept': 'application/vnd.pagerduty+json;version=2'}
        response = self.session.get('https://api.pagerduty.com/abilities',
                                    headers=self.headers, auth=self.auth)
        response.raise_for_status()

    def fetch_incidents_between(self, start, end):
        self.logger.info('fetching messages between %s and %s',
                         start.isoformat(), end.isoformat())

        params = {'since': start.isoformat(),
                  'until': end.isoformat(),
                  'limit': '100'}
        incidents = []

        response = self.session.get('https://api.pagerduty.com/incidents',
                                    headers=self.headers, auth=self.auth,
                                    params=params)
        response.raise_for_status()
        body = response.json()
        incidents.extend(body['incidents'])
        while body['more']:
            params['offset'] = body['offset'] + body['limit']
            response = self.session.get('https://api.pagerduty.com/incidents',
                                        headers=self.headers, auth=self.auth,
                                        params=params)
            response.raise_for_status()
            body = response.json()
            incidents.extend(body['incidents'])

        self.logger.debug('found %d incidents', len(incidents))
        return incidents


def list_incidents():
    logger = _logger.getChild('list_incidents')
    cli.configure_logging()
    api_token = cli.require_environment(logger, 'PAGERDUTY_TOKEN')

    if len(sys.argv) < 2:
        prog_name = pathlib.Path(sys.argv[0]).stem
        sys.stderr.write('Usage: {} START END\n'.format(prog_name))
        sys.exit(os.EX_USAGE)

    conn = Connection(api_token)
    start = maya.parse(sys.argv[1]).datetime()
    end = maya.parse(sys.argv[2]).datetime()
    incidents = conn.fetch_incidents_between(start, end)
    logger.info('found %d messages', len(incidents))
    json.dump(sorted(incidents, key=_extract_timestamp), sys.stdout,
              sort_keys=True)


def _extract_timestamp(incident):
    return maya.parse(incident['created_at'])
