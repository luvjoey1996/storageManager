from flask import Flask
from flask_apscheduler import APScheduler
from flask_peewee.db import Database

app = Flask("storageManager")
app.config.from_object('config.Configuration')

scheduler = APScheduler()
scheduler.init_app(app)

db = Database(app)
