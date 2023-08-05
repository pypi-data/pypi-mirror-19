record-ip-to-dnspod
===================

Record machine's ip to DNSpod via `DNSPod's API`_.

Installation
------------

To install::

    pip install record-ip-to-dnspod


Example Usage
-------------

Command::

    record-ip-to-dnspod -c /path/record-ip.ini


If you wan't install via pip, you can::

    git clone https://github.com/codeif/record-ip-to-dnspod.git
    cd record-ip-to-dnspod && python -m record_ip_to_dnspod.bin -c /path/record-ip.ini


Config Example
--------------

ini文件::

    [record-ip]
    log-path = record-ip.log
    token = 1234,your-token-str
    email = me@codeif.com
    domain = example.com
    sub-domain = test
    ; interface = eth0
    ; exclude-ips = 127.0.0.1,172.16.0.1


Config Options
--------------

- 必填配置项

===========     ================================================================
配置项          说明
===========     ================================================================
log-path        日志路径
token           Token_, 例如：13490,6b5976c68aba5b14a0558b77c17c3932&format=json
email           联系邮箱，用于API请求的User-Agent.
domain          域名， 例如： example.com
sub-domain      主机记录, 如 www，可选，如果不传，默认为 @
===========     ================================================================


- 可选配置项

===========     ================================================================
配置项          说明
===========     ================================================================
interface       只记录指定的网卡，例如: eth0
excluet-ips     不记录下面的ip， 比如'127.0.0.1,172.16.0.1'
===========     ================================================================


.. _Token: https://support.dnspod.cn/Kb/showarticle/tsid/227
.. _DNSPod's API: http://www.dnspod.cn/docs/index.html
