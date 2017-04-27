#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml


INVENTORY_FILE = 'Please override here.'
VARS_FILE = 'Please override here.'


class RegisterVars(object):
    def __init__(self):
        'This class has no propertys.'

    def _open_file(self, arglist):
        targetfile = arglist[0]
        return lambda flag: [open(targetfile, flag), arglist[1]]
    
    def _close_file(self, resultlist):
        resultlist[0].close()
        return resultlist
    
    def _refine_param(self, host_ip_list):
        'Please override here.'
    
    def _generate_hostlist(self, resultlist):
        'Please override here.'

    def _register_varsfile(self, resultlist):
        host_ip_list = resultlist[1]
        param_dict = self._refine_param(host_ip_list)
        resultlist[0].write(yaml.dump(param_dict))
        return resultlist
    
    def _flow(self, arglist):
        return lambda flag: (
                   lambda func: self._close_file( func( self._open_file(arglist)(flag) ) )
               )
    
    def main(self, INVENTORY_FILE, VARS_FILE):
        read_arglist = [INVENTORY_FILE, []]
        host_ip_list = self._flow(read_arglist)('r')(self._generate_hostlist)[1]
    
        write_arglist = [VARS_FILE, host_ip_list]
        self._flow(write_arglist)('w')(self._register_varsfile)
    
