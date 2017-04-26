#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from register_vars import RegisterVars


INVENTORY_FILE = './hosts'
VARS_FILE = './group_vars/servers.yml'


class RegisterHostsVars(RegisterVars):
    def __init__(self):
        super(RegisterHostsVars, self).__init__()
        'This class has no propertys.'

    def _generate_hostlist(self, resultlist):
        resultlist[1] = map(lambda n:n.strip().split(' mngip='),
                            filter(lambda n:'mngip' in n and not re.match('\A#', n), resultlist[0]))
        return resultlist

    def _refine_each_param(self, host_ip_list, param_dict):
        host_ip_list.reverse()
        if not host_ip_list:
            return param_dict
        host_ip = host_ip_list.pop()
        param_dict['hosts_params'].append({'name':host_ip[0], 'ipaddr':host_ip[1]})
        return self._refine_each_param(host_ip_list, param_dict)
    
    def _refine_param(self, host_ip_list):
        param_dict = {'hosts_params': []}
        return self._refine_each_param(host_ip_list, param_dict)

if __name__ == '__main__':
    RegisterHostsVars().main(INVENTORY_FILE, VARS_FILE)

