import requests
import json


class Localytics:
    """https://dashboard.localytics.com/settings/apikeys"""


    def __init__(self, app_id, api_key, api_secret):
        self.url = 'https://messaging.localytics.com/v2/push/{app_id}'.format(app_id=app_id)

        self.session = requests.Session()
        self.session.auth = (api_key, api_secret)
        self.session.headers.update({'Content-Type': 'application/json'})

    def push(self, target_type, messages, all_devices=None, request_id=None, campaign_key=None):
        data = {'target_type': target_type, 'messages': messages}

        add_key_to_dict(data, 'request_id', request_id)
        add_key_to_dict(data, 'campaign_key', campaign_key)
        data.setdefault('campaign_key', 'null')
        add_key_to_dict(data, 'all_devices', all_devices)

        self._request(data)

    def _request(self, data):
        r = self.session.post(self.url, data=json.dumps(data))
        # Sometimes they send HTML pages instead of json and that always means
        # error occurred.
        if r.headers['Content-Type'] != 'application/json; charset=utf-8':
            raise LocalyticsHTTPError(r.status_code, r.text)
        if r.status_code != 202:
            raise LocalyticsHTTPError(r.status_code, r.json()['error'])


def add_key_to_dict(d, key, value):
    if value == None:
        return d
    d[key] = value
    return d

class LocalyticsHTTPError(Exception):

    def __init__(self, code, message):
        self.code = code
        self.message = message
