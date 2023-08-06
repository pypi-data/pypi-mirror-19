import json
import logging
import os
import pathlib
import sys
import urllib.parse

import maya
import requests

from ictools import auth, cli


_logger = logging.getLogger(__name__)


class Connection(object):

    def __init__(self, access_token):
        self.logger = _logger.getChild('Connection')
        self.auth = auth.HTTPBearerAuth(access_token)
        self.session = requests.Session()
        response = self.session.get(
            'https://api.hipchat.com/v2/room?auth_test=true',
            auth=self.auth)
        response.raise_for_status()

    def fetch_messages(self, room, start, end):
        logging.getLogger('requests').setLevel(logging.DEBUG)
        self.logger.info('fetching messages from %s between %s and %s',
                         room, start.isoformat(), end.isoformat())
        response = self.session.get(
            'https://api.hipchat.com/v2/room/{}/history'.format(
                urllib.parse.quote(room)), auth=self.auth,
            params={'date': end.isoformat(), 'end-date': start.isoformat()})
        if response.status_code == 404:
            self.logger.error('room %s not found', room)
            return None
        response.raise_for_status()
        items = response.json()['items']
        for item in items:
            item['room'] = room
        return items


def scan_room():
    logger = _logger.getChild('scan_room')
    cli.configure_logging()
    api_token = cli.require_environment(logger, 'HIPCHAT_TOKEN')

    if len(sys.argv) < 3:
        prog_name = pathlib.Path(sys.argv[0]).stem
        sys.stderr.write(
            'Usage: {} START END ROOM [ROOM...]\n'.format(prog_name))
        sys.exit(os.EX_USAGE)

    conn = Connection(api_token)
    earliest = maya.parse(sys.argv[1]).datetime()
    latest = maya.parse(sys.argv[2]).datetime()
    messages = []
    for room in sys.argv[3:]:
        items = conn.fetch_messages(room, earliest, latest)
        logger.debug('found %d messages in %d', len(items), room)
        messages.extend(items)

    logger.info('found %d messages', len(messages))
    json.dump(sorted(messages, key=_extract_timestamp), sys.stdout)


def _extract_timestamp(msg_data):
    return maya.parse(msg_data['date'])
