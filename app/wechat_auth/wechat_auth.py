#!/usr/bin/env python3
# coding: utf8
# 20170119 anChaOs


# general
import json, time
import requests # for http requests
from datetime import datetime, timedelta, date

# flask
from flask import Flask, request, redirect

# config
import config as config

# database
import app.database.api as dbapi

# flask-app
from app import app


# const
APP_ID = config.APP_ID
APP_SECRET = config.APP_SECRET
REDIRECT_URI = config.REDIRECT_URI
JUMP_URL = config.JUMP_URL


@app.route('/')
def index():
    return 'Ok'


@app.route('/wechat_auth/')
def wechat_auth():
    if 'code' in request.args:
        state = request.args.get('state', '')
        code  = request.args.get('code', '')
        err, user_info = get_user_info(code)
        if err:
            return 'wechat error'
        else:
            user = dbapi.get_user(user_info)
            if user:
                data = to_dict(user)
                data.pop('utime')
                data.pop('ctime')
                url = JUMP_URL + str(user.id)
                return redirect(url)
                return json.dumps(data)
            else:
                return 'user db error'
    else:
        url = gen_auth_url()
        return redirect(url)


def to_dict(self):
  return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}



"""
    @微信网页身份授权

        *   `微信公众号` 网页授权 (https://mp.weixin.qq.com/wiki)

"""
def gen_auth_url(state="STATE", redirect_uri=REDIRECT_URI):
    urlbase  = "https://open.weixin.qq.com/connect/oauth2/authorize"
    print("[Redirect] %s\n%s", redirect_uri, REDIRECT_URI)
    params = {
        "appid": APP_ID,
        "redirect_uri" : redirect_uri,    # urllib.quote_plus(AuthCodeHandler)
        "response_type": "code",
        "scope": "snsapi_userinfo",       # snsapi_base | snsapi_userinfo
        "state": state
    }
    # 排序params
    str_params = '&'.join(['%s=%s' % (key.lower(), params[key])
                           for key in sorted(params)])
    auth_url = urlbase + "?" + str_params + "#wechat_redirect"
    return auth_url


def get_user_access_token(code):
    url    = "https://api.weixin.qq.com/sns/oauth2/access_token"
    params = {
        "appid" : APP_ID,
        "secret": APP_SECRET,
        "code"  : code,
        "grant_type": "authorization_code"
    }
    r = requests.get(url, params=params)
    if r.status_code == 200:
        result = r.json()
        if "errcode" not in result:
            return (None, result)
        else:
            return (r.content, None)
    else:
        return (r.content, None)


def get_user_info(code):
    err, res = get_user_access_token(code)
    if err or not res:
        return (err, None)
    url    = "https://api.weixin.qq.com/sns/userinfo"
    params = {
        "access_token": res['access_token'],
        "openid"      : res['openid'],
        "lang"        : "zh_CN"
    }
    r = requests.get(url, params=params)
    if r.status_code == 200:
        user_info = json.loads(r.content.decode("utf8"))
        if "errcode" not in user_info:
            return (None, user_info)
        else:
            return (r.content, None)
    else:
        return (r.content, None)