import os

from flask import Flask
from flask import render_template
from flask.ext.sqlalchemy import SQLAlchemy
from models import *

from database import db_session

IS_HEROKU = 'IS_HEROKU' in os.environ

app = Flask(__name__)
if IS_HEROKU:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////%s/db/test.db' % os.path.dirname(os.path.realpath(__file__))
db = SQLAlchemy(app)

@app.route('/')
def admin_dashboard():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)


@app.route('/robots.txt')
def robots():
    res = app.make_response('User-agent: *\nAllow: /')
    res.mimetype = 'text/plain'
    return res

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
