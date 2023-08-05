# -*- coding: utf-8 -*-
import logging
import json
from .compat import urlencode, Request, urlopen


class DNSPodClient(object):

    def __init__(self, token, user_agent, domain, sub_domain):

        self.token = token
        self.domain = domain
        self.sub_domain = sub_domain
        self.headers = {
            'User-Agent': user_agent,
        }

    def _post(self, path, data={}):
        url = 'https://dnsapi.cn{}'.format(path)
        req_data = {
            'login_token': self.token,
            'format': 'json',
            'lang': 'cn',
            'error_on_empty': 'no',
        }
        req_data.update(data)
        req_data = urlencode(req_data).encode('utf-8')
        req = Request(url, req_data, self.headers)
        resp = urlopen(req)
        content = resp.read().decode('utf-8')
        logging.info('DNSPodClient post data:\nurl: %s\ndata: %s\n'
                     'response: %s', url, data, content)
        return json.loads(content)

    def version(self):
        path = '/Info.Version'
        return self._post(path)

    def user_detail(self):
        path = '/User.Detail'
        return self._post(path)

    def domain_log(self):
        path = '/Domain.Log'
        data = {
            'domain': self.domain
        }
        return self._post(path, data)

    def domain_info(self):
        path = '/Domain.Info'
        data = {
            'domain': self.domain
        }
        return self._post(path, data)

    def record_list(self):
        """记录列表"""
        path = '/Record.List'
        data = {
            'domain': self.domain,
            'sub_domain': self.sub_domain,

        }
        return self._post(path, data)

    def record_create(self, ip):
        """创建记录"""
        path = '/Record.Create'
        data = {
            'domain': self.domain,
            'sub_domain': self.sub_domain,
            'record_type': 'A',
            'record_line': '默认',
            'value': ip,
        }
        return self._post(path, data)

    def record_remove(self, record_id):
        """删除记录"""
        path = '/Record.Remove'
        data = {
            'domain': self.domain,
            'record_id': record_id,
        }
        return self._post(path, data)

    def record_modify(self, record_id, ip):
        path = '/Record.Modify'
        data = {
            'domain': self.domain,
            'record_id': record_id,
            'sub_domain': self.sub_domain,
            'record_type': 'A',
            'record_line': '默认',
            'value': ip,
        }
        return self._post(path, data)
