#!/bin/bash

python register_hosts_vars.py
python check_inventory.py
ansible-playbook -i hosts `pwd`/site.yml
