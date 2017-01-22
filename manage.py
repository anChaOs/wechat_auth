#!/usr/bin/env python3
#coding: utf8

import os

from flask import Flask
from flask.ext.script import Manager

from app import app

manager = Manager(app)


if __name__ == '__main__':
    manager.run()