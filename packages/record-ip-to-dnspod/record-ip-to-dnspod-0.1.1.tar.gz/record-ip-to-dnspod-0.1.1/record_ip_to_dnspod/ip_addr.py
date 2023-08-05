# -*- coding: utf-8 -*-

"""
record_ip_to_dnspod.ip_addr
~~~~~~~~~~~~~~~~~~~~~~~~~~~

使用ifconfig命令获取机器IP额模块
"""

import os
import re


def get_ips(interface=None):
    """返回IP列表"""
    command = '$(which ifconfig)'
    if interface:
        command = '{} {}'.format(command, interface)
    with os.popen(command) as f:
        content = f.read()

    return re.findall('inet (?:addr:)?(\d+\.\d+.\d+.\d+)', content)


if __name__ == '__main__':
    print(get_ips())
