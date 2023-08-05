# -*- coding: utf-8 -*-
from datetime import datetime
import argparse
import os.path
import logging

from . import __version__
from . import ip_addr
from .compat import ConfigParser, is_str
from .dnspod import DNSPodClient


parser = argparse.ArgumentParser(
    description='Record ip to DNSPod.')
parser.add_argument('-c', '--config', required=True)


def operation_record(client, interface, exclude_ips):
    if is_str:
        exclude_ips = set(exclude_ips.replace(' ', '').split(','))
    local_ips = set(ip_addr.get_ips(interface)) - exclude_ips
    logging.info('local ips: %s', local_ips)
    if not local_ips:
        logging.info('no local ips, return')
        return
    record_list = client.record_list()

    record_dict = {}
    for record in record_list['records']:
        record_dict[record['value']] = record['id']
    logging.info('record_dict: %s', record_dict)

    remote_ips = set(record_dict.keys())

    remove_ips = list(remote_ips - local_ips)
    new_ips = list(local_ips - remote_ips)
    modify_count = min(len(remove_ips), len(new_ips))
    logging.info('remove_ips: %s, new_ips: %s', remove_ips, new_ips)
    for i in range(modify_count):
        remove_ip = remove_ips[i]
        new_ip = new_ips[i]

        record_id = record_dict[remove_ip]
        result = client.record_modify(record_id, new_ip)
        logging.info('modify record_id-%s, remove_ip-%s add new_ip-%s',
                     record_id,
                     remove_ip,
                     new_ip)

        remove_ips.remove(remove_ip)
        new_ips.remove(new_ip)

    logging.info('remove_ips: %s, new_ips: %s', remove_ips, new_ips)

    for ip in remove_ips:
        result = client.record_remove(record_dict[ip])
        logging.info('remove ip-%s, result-%s', ip, result)

    for ip in new_ips:
        result = client.record_create(ip)
        logging.info('add ip-%s, result-%s', ip, result)


def main():
    parsed_args = parser.parse_args()
    ini_path = os.path.abspath(parsed_args.config)
    config_parser = ConfigParser()
    config_parser.read(ini_path)
    options = dict(config_parser.items('record-ip'))

    token = options.get('token')
    email = options.get('email')
    domain = options.get('domain')
    sub_domain = options.get('sub-domain')
    interface = options.get('interface')
    exclude_ips = options.get('exclude-ips', '127.0.0.1')
    log_path = os.path.abspath(options['log-path'])

    logging.basicConfig(filename=log_path, level=logging.DEBUG)
    logging.info('\n\n ******* push ip exec start at: %s *******',
                 datetime.now())

    assert token and email and domain and sub_domain

    user_agent = 'Record IP to DNSPod Client/{}({})'.format(__version__, email)
    client = DNSPodClient(token, user_agent, domain, sub_domain)

    operation_record(client, interface, exclude_ips)
    logging.info('finish')


if __name__ == '__main__':
    main()
