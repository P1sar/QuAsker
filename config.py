import os 
CSRF_ENABLED = True
SECRET_KEY = "Very_Secret_Key"

basedir = os.path.abspath(os.path.dirname(__file__))



SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

#Full-text search settings 
WHOOSH_BASE = os.path.join(basedir, 'search.db')
MAX_SEARCH_RESULTS = 50