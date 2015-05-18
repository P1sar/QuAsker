from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.social import Social
from flask.ext.login import LoginManager
from config import basedir


app=Flask(__name__)
app.config.from_object("config")
db=SQLAlchemy(app)
lm=LoginManager()
lm.init_app(app)
lm.login_view = 'login'

app.config['SOCIAL_FACEBOOK'] = {
    'consumer_key': '1603992546481877',
    'consumer_secret': 'e78dd356274d3c73c497f1e6c6a9554d'
}

from app import views, models