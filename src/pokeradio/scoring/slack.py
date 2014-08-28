import json
import requests
import logging

from django.conf import settings

logger = logging.getLogger('raven')


class Slack:
    DEV = 1
    PUBLIC = 2

    GENERAL = '#general'
    USERNAME = "Poke Radio"

    PINK = '#f5007f'

    def __init__(self, pretext, fallback='', colour=PINK,
                 channel=GENERAL, group=DEV):

        self.url = {self.DEV: settings.DEV_SLACK_WEBHOOK_URL,
                    self.PUBLIC: settings.EVERYONE_SLACK_WEBHOOK_URL}[group]

        self.colour = colour
        self.pretext = pretext
        self.fallback = fallback
        self.channel = channel

        self.fields = []

    def add_field(self, title, value, short=False):
        self.fields.append({'title': title, 'value': value, 'short': short})

    def _get_payload(self):
        return {
            'username': self.USERNAME,
            'channel': self.channel,
            'pretext': self.pretext,
            'fallback': self.fallback,
            'color': self.colour,
            'fields': self.fields,
        }

    def send(self):
        payload = self._get_payload()
        if not settings.SLACK:
            print 'Slack message', payload
            return
        try:
            r = requests.post(self.url, data=json.dumps(payload))
        except Exception, e:
            logger.warn('cannot send data to Slack')
