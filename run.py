#!flask/bin/python

#Just script to start the app

from app import app
app.run(debug = True, host='0.0.0.0')