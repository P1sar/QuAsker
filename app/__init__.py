from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.social import Social
from flask.ext.login import LoginManager
from config import basedir
from flask_oauth import OAuth

oauth = OAuth()
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


facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key="1603992546481877",
    consumer_secret="e78dd356274d3c73c497f1e6c6a9554d",
    request_token_params={'scope': 'email'}
)

from app import views, models