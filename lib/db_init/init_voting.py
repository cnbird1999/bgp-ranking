#!/usr/bin/python
# -*- coding: utf-8 -*-


import os 
import sys
import ConfigParser
config = ConfigParser.RawConfigParser()
config.read("../../etc/bgp-ranking.conf")
root_dir = config.get('directories','root')
sys.path.append(os.path.join(root_dir,config.get('directories','libraries')))

from db_models.voting import *

voting_metadata.drop_all()
voting_metadata.create_all()

# Creation of the admin user, with default password
Users(login=unicode('admin'), password=unicode('admin'))

v_session = VotingSession()
v_session.commit()
v_session.close()