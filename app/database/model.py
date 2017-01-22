#!/usr/bin/env python3
# coding: utf8
# 20170119 anChaOs

import json

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text

from app import db


class User(db.Model):
    __tablename__ = 'user'

    id          = Column(Integer, primary_key=True)
    openid      = Column(String(256), index=True, nullable=False, server_default="", unique=True)
    unionid     = Column(String(256), index=True, nullable=False, server_default="")
    nickname    = Column(String(128), nullable=True, server_default="")
    sex         = Column(String(1), nullable=False, server_default="0")
    province    = Column(String(64), nullable=False, server_default="")
    city        = Column(String(64), nullable=False, server_default="")
    country     = Column(String(64), nullable=False, server_default="")
    headimgurl  = Column(String(512), nullable=False, server_default="")
    privilege   = Column(Text)
    ctime       = Column(DateTime, nullable=False)
    utime       = Column(DateTime, nullable=False)

    def __init__(self, body):
        self.openid     = body['openid']
        self.nickname   = body['nickname']
        self.sex        = body['sex']
        self.province   = body['province']
        self.city       = body['city']
        self.country    = body['country']
        self.headimgurl = body['province']
        if isinstance(body['privilege'], list):
            body['privilege'] = json.dumps(body['privilege'])
        self.privilege = body['privilege']
        if 'unionid' in body:
            self.unionid = body['unionid']
        dt = datetime.now()
        self.utime = dt
        self.ctime = dt

    def __repr__(self):
        return '<User %r>' % self.nickname
