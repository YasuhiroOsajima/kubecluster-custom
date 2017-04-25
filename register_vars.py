#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import yaml


INVENTORY_FILE = './hosts.example'
VARS_FILE = './group_vars/all.yml'


def open_file(arglist):
    targetfile = arglist[0]
    return lambda flag: [open(targetfile, flag), arglist[1]]

def close_file(resultlist):
    resultlist[0].close()
    return resultlist

def split_host_ip(resultlist):
    resultlist[1] = map(lambda n:n.strip().split(' mngip='),
                        filter(lambda n:'mngip' in n, resultlist[0]))
    return resultlist
 
def register_vars(resultlist):
    host_ip_list = resultlist[1]
    param_dict = refine_param(host_ip_list)
    resultlist[0].write(yaml.dump(param_dict))
    return resultlist

def refine_param(host_ip_list):
    host_ip_list.reverse()
    param_dict = {'hosts_params': []}
    return refine_each_param(host_ip_list, param_dict)

def refine_each_param(host_ip_list, param_dict):
    if not host_ip_list:
        return param_dict
    host_ip = host_ip_list.pop()
    param_dict['hosts_params'].append({'name':host_ip[0], 'ipaddr':host_ip[1]})
    return refine_each_param(host_ip_list, param_dict)

def func_file(arglist):
    return lambda flag: (
               lambda func: close_file( func( open_file(arglist)(flag) ) )
           )


if __name__ == '__main__':
    read_arglist = [INVENTORY_FILE, []]
    host_ip_list = func_file(read_arglist)('r')(split_host_ip)[1]

    write_arglist = [VARS_FILE, host_ip_list]
    func_file(write_arglist)('w')(register_vars)

