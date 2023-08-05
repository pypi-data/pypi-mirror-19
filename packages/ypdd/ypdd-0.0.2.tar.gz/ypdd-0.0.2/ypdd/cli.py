# coding: utf-8

import click

from ypdd.conf import Config
from ypdd.core import AddSubDomain, DelSubDomain


@click.group()
def cli():
    pass


@cli.command('add-domain')
@click.argument('domain')
@click.argument('rtype')
@click.argument('sub-domain')
@click.argument('content')
def add_domain(domain, rtype, sub_domain, content):
    """ Adding sub-domain """

    conf = Config()
    add_sub_domain = AddSubDomain(
        pdd_token=conf.pdd_token,
        domain=domain,
        rtype=rtype,
        sub_domain=sub_domain,
        content=content
    )

    print(add_sub_domain.request)


@cli.command('del-domain')
@click.argument('domain')
@click.argument('record-id')
def del_domain(domain, record_id):
    """ Deleting sub-domain """

    conf = Config()
    del_sub_domain = DelSubDomain(conf.pdd_token, domain, record_id)

    print(del_sub_domain.request)
