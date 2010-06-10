# -*- coding: utf-8 -*-
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.schema import ThreadLocalMetaData
from elixir import *

import os
precdir = os.path.realpath(os.curdir)
os.chdir(os.path.dirname(__file__))
import ConfigParser
config = ConfigParser.RawConfigParser()
config.read("../../etc/bgp-ranking.conf")
login = config.get('mysql','login')
password = config.get('mysql','password')
host = config.get('mysql','hostname')
dbname = config.get('mysql','dbname_ranking')
os.chdir(precdir)

ranking_engine = create_engine( 'mysql://' + login + ':' + password + '@' + host + '/' + dbname )
RankingSession = scoped_session(sessionmaker(bind=ranking_engine))
ranking_metadata = ThreadLocalMetaData()
ranking_metadata.bind = ranking_engine

import datetime 

INET6_ADDRSTRLEN = 46

class IPs(Entity):
    """ 
    Table which contains the IPs 
    """
    ip = Field(Unicode(INET6_ADDRSTRLEN), primary_key=True)
    ip_descriptions = OneToMany('IPsDescriptions')
    using_options(metadata=ranking_metadata, session=RankingSession, tablename='IPs')
    
    def __repr__(self):
        return 'IP: "%s"' % (self.ip)


class IPsDescriptions(Entity):
    """ 
    Table which contains a description of the IPs
    and a link to the ASNs Descriptions 
    """
    list_name = Field(UnicodeText, required=True)
    timestamp = Field(DateTime(timezone=True), default=datetime.datetime.utcnow)
    list_date = Field(DateTime(timezone=True), required=True)
    times = Field(Integer, default=1)
    infection = Field(UnicodeText, default=None)
    raw_informations = Field(UnicodeText, default=None)
    whois = Field(Binary)
    whois_address = Field(UnicodeText)
    ip = ManyToOne('IPs')
    asn = ManyToOne('ASNsDescriptions')
    using_options(metadata=ranking_metadata, session=RankingSession, tablename='IPsDescriptions')
  
    def __repr__(self):
        to_return = '[%s] List: "%s" \t %s present %s time(s)' % (self.list_date, self.list_name,\
                    self.ip,  self.times)
        if self.asn:
            to_return += '\t %s' % (self.asn.asn)
        return to_return

    
class ASNs(Entity):
    """ 
    Table which contains the ASNs 
    """
    asn = Field(Integer, primary_key=True)
    asn_description = OneToMany('ASNsDescriptions')
    using_options(metadata=ranking_metadata, session=RankingSession, tablename='ASNs')
  
    def __repr__(self):
        return 'ASN: "%s"' % (self.asn)
  

class ASNsDescriptions(Entity):
    """ 
    Table which contains a description of the ASNs
    and a link to the IPs Descriptions 
    """
    timestamp = Field(DateTime(timezone=True), default=datetime.datetime.utcnow)
    owner = Field(UnicodeText, required=True)
    ips_block = Field(Unicode(INET6_ADDRSTRLEN), required=True)
    riswhois_origin = Field(UnicodeText)
    asn = ManyToOne('ASNs')
    ips = OneToMany('IPsDescriptions')
    using_options(metadata=ranking_metadata, session=RankingSession, tablename='ASNsDescriptions')
  
    def __repr__(self):
        return '[%s] %s \t Owner: "%s" \t Block: "%s"' % (self.timestamp,\
                self.asn, self.owner, self.ips_block)


setup_all()