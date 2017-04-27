#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from register_vars import RegisterVars

INVENTORY_FILE = './hosts'
VARS_FILE = './group_vars/cluster.yml'


class CheckInventory(RegisterVars):
    def __init__(self):
        super(CheckInventory, self).__init__()
        'This class has no propertys.'

    def _select_host(self, fileline_list, patern):
        masterhosts = []
        flag = 0
        for row in fileline_list:
            if patern in row:
                flag = 1
                continue
            if 'mngip' in row and not re.match('\A#', row) and flag:
                masterhosts.append(row)
                continue
            if '[' in row:
                flag = 0

        return  map(lambda n:n.strip().split(' mngip='), masterhosts)

    def _generate_hostlist(self, resultlist):
        resultlist[0].seek(0)
        fileline_list = resultlist[0].readlines()

        mastarts = self._select_host(fileline_list, '[master]')
        loadbalancers = self._select_host(fileline_list, '[loadbalancer]')

        resultlist[1] = {'masters': mastarts, 'loadbalancers': loadbalancers}
        return resultlist

    def _refine_param(self, host_ip_list):
        masters = map(lambda n: n[0], host_ip_list['masters'])
        if len(host_ip_list['masters']) > 1:
            clustermember = ','.join(map(lambda n: "%s=http://%s:2380" % (n[0], n[1]),
                                         host_ip_list['masters']))
            return ({'clusterd': True,
                     'masterip': host_ip_list['loadbalancers'][0][1],
                     'masters': masters,
                     'clustermember': clustermember})
        else:
            return ({'clusterd': False,
                     'masterip': host_ip_list['masters'][0][1],
                     'masters': masters})


if __name__ == '__main__':
    CheckInventory().main(INVENTORY_FILE, VARS_FILE)

