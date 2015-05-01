import json
import requests
import logging

from django.conf import settings

logger = logging.getLogger('raven')


class Slack:

    GENERAL = '#general'
    USERNAME = "Poke Radio"

    PINK = '#f5007f'

    def __init__(self, pretext, fallback='', colour=PINK, channel=GENERAL):


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
            r = requests.post(settings.DEV_SLACK_WEBHOOK_URL,
                              data=json.dumps(payload))
        except Exception, e:
            logger.warn('Cannot send data to Slack')
