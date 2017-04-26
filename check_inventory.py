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

    def _select_host(self, resultlist, patern):
        resultlist[0].seek(0)
        masterhosts = []
        flag = 0
        for row in resultlist[0].readlines():
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
        mastarts = self._select_host(resultlist, '[master]')
        loadbalancers = self._select_host(resultlist, '[loadbalancer]')

        resultlist[1] = {'masters': mastarts, 'loadbalancers': loadbalancers}
        return resultlist

    def _refine_param(self, host_ip_list):
        if len(host_ip_list['masters']) > 1:
            return {'clusterd': True, 'masterip': host_ip_list['loadbalancers'][0][1]}
        else:
            return {'clusterd': False, 'masterip': host_ip_list['masters'][0][1]}


if __name__ == '__main__':
    CheckInventory().main(INVENTORY_FILE, VARS_FILE)

