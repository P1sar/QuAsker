from flask import Flask
from flask_sqlalchemy import SQLAlchemy
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





facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key="1603992546481877",
    consumer_secret="e78dd356274d3c73c497f1e6c6a9554d",
    request_token_params={'scope': 'email'}
)

app.config['UPLOAD_FOLDER'] = 'D:/FlaskProjects/QuAsker/app/static/avatars'
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

from app import views, models