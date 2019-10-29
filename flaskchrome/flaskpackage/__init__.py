import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from logging import DEBUG

app = Flask(__name__)
app.logger.setLevel(DEBUG)
basedir = os.path.abspath(os.path.dirname(__file__))
app.secret_key = "super secret key"
app.config["SECRET KEY"] = 'filesystem'
x = app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'flaskchrome.db')
db = SQLAlchemy(app)

from flaskpackage.routes import route_delete
from flaskpackage.routes import route_run
from flaskpackage.routes import route_execute


# import webbrowser
# from selenium import webdriver
# driver = webdriver.Chrome()
# webbrowser.open_new_tab('http://localhost:9000')
