# coding: utf-8

import urllib.parse

import requests


class YPddBase:
    def __init__(self, pdd_token, domain):
        self.pdd_token = pdd_token
        self.domain = domain
        self.url = 'https://pddimp.yandex.ru'

    def __getattr__(self, item):
        try:
            return getattr(self.result, item, None)
        except AttributeError:
            return None

    def post(self, **data):
        return requests.post(
            self.url, data, headers={'PddToken': self.pdd_token})

    def request(self):
        raise RuntimeError()


class AddSubDomain(YPddBase):
    def __init__(self, pdd_token, domain, rtype, sub_domain, content):
        super(AddSubDomain, self).__init__(pdd_token, domain)

        self.url = urllib.parse.urljoin(self.url, '/api2/admin/dns/add')
        self.data = {
            'domain': self.domain, 'type': rtype, 'subdomain': sub_domain,
            'content': content
        }

        self.answer = None

    @property
    def request(self):
        self.answer = self.post(**self.data)
        return self.answer.json()


class DelSubDomain(YPddBase):
    def __init__(self, pdd_token, domain, record_id):
        super(DelSubDomain, self).__init__(pdd_token, domain)

        self.url = urllib.parse.urljoin(self.url, '/api2/admin/dns/del')
        self.data = {
            'domain': self.domain, 'record_id': record_id
        }

        self.answer = None

    @property
    def request(self):
        self.answer = self.post(**self.data)
        return self.answer.json()
