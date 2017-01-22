#!/usr/bin/env python3
# coding: utf8
# 20170119 anChaOs

import traceback

from app import db
from .model import *


def make_new_user(body):
    try:
        user = User(body)
        db.session.add(user)
        db.session.commit()
        return user
    except:
        traceback.print_exc()
        return None


def get_user(body):
    try:
        openid = body['openid']
        user = db.session.query(User).filter(User.openid==openid).first()
        if not user:
            user = make_new_user(body)
        return user
    except:
        traceback.print_exc()
        return None

