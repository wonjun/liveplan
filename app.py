import os

from flask import Flask
from flask import render_template
from flask.ext.sqlalchemy import SQLAlchemy
from models import *

IS_HEROKU = 'IS_HEROKU' in os.environ

app = Flask(__name__)
if IS_HEROKU:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////%s/db/test.db' % os.path.dirname(os.path.realpath(__file__))
db = SQLAlchemy(app)

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    projects = Project.query.all()    
    return render_template('admin_dashboard.html', projects=projects)

@app.route('/admin_dashboard/create_project')
def create_project():
    return render_template('create_project.html')

@app.route('/admin_dashboard/project/tasks')
def project_tasks():
    return render_template('project_tasks.html')

@app.route('/admin_dashboard/project/users')
def project_users():
    return render_template('project_users.html')

@app.route('/admin_dashboard/project/create_user')
def create_user():
    return render_template('create_user.html')

@app.route('/admin_dashboard/project/create_task')
def detail_project_view():
    return render_template('create_task.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
