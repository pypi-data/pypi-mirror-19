import analogbridge
import json
from requests import Request, Session


class APIRequest(object):
    def __init__(self, url, method=None, params=None, key_required=True):
        self.url = url
        if not method:
            method = "GET"
        self.method = method
        try:
            self.params = json.dumps(params)
            self.headers = {'Content-Type': 'application/json'}
        except:
            self.params = None
        self.key_required = key_required
        self.resp = None
        self.status_code = None
        self.message = None
        self.data = None
        self.error = None


    def call(self):
        if not analogbridge.api_version:
            analogbridge.api_version = analogbridge.default_api_version

        if self.key_required and not analogbridge.api_key:
            raise Exception("api secret key required")

        s = Session()
        req = Request(self.method, self.build_url(), headers=self.headers, data=self.params,
                      auth=(analogbridge.api_key, ''))
        prepped = req.prepare()
        self.resp = s.send(prepped)

        self.handle_response()

        return self.data


    def build_url(self):
        return analogbridge.api_base + "/" + analogbridge.api_version + "/" + self.url

    def handle_response(self):
        self.status_code = self.resp.status_code

        if self.status_code < 200 or self.status_code >= 300:
            self.error = True
            self.message = self.resp.json()
            raise Exception(self.message)
        else:
            self.message = self.resp.json()['message'] if 'message' in self.resp.json() else None
            self.data = self.resp.json()['data'] if 'data' in self.resp.json() else self.resp.json()

        return self.data