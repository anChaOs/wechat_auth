from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from config import config


db = SQLAlchemy()
app = Flask(__name__)
app.config.from_object(config.config_list['default'])
config.config_list['default'].init_app(app)

db.init_app(app)

# ======= this should at last ========
from app import database
from app import wechat_auth
