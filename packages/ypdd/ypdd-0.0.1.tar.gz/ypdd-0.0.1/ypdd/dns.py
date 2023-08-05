# coding: utf-8

import requests


def get_domains(token):
    """
    Getting domains.

    :param token: PddToken
    :type token: str
    :return: dict
    """
    url = 'https://pddimp.yandex.ru/api2/admin/domain/domains'

    r = requests.get(url, headers={'PddToken': token})

    if r.status_code != 200:
        return {}
    else:
        return r.json()


def get_records(token, domain):
    url = 'https://pddimp.yandex.ru/api2/admin/dns/list'

    r = requests.get(
        url, params={'domain': domain}, headers={'PddToken': token})

    if r.status_code != 200:
        return {}
    else:
        return r.json()


def add_record(token, domain, _type, subdomain, content):
    url = 'https://pddimp.yandex.ru/api2/admin/dns/add'

    r = requests.post(
        url, data={'domain': domain, 'type': _type, 'subdomain': subdomain,
                   'content': content}, headers={'PddToken': token})

    if r.status_code != 200:
        return {}
    else:
        return r.json()
