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
def home(admin=None):
  return render_template('index.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    # look at models functions later to change
    projects = Project.query.all()    
    return render_template('admin_dashboard.html', projects=projects)

@app.route('/admin_dashboard/create_project')
def create_project():
    # look at models functions later to change
    error = None
    if request.method == 'POST':
        if not request.form['name']:
            error = 'You do not have a name'
        elif not request.form['description']:
            error = 'You do not have a description'
        else:
            # db magic insert and save as project
            flash('You have successfully created a project!')
            return redirect(url_for('/admin_dashboard/')) # + project.id))
    return render_template('create_project.html', error=error)

@app.route('/admin_dashboard/<project>/<action>')
def project_tasks(project = None, action = None):
    if action == 'detail_task':
        return render_template('project_tasks.html', project=project)
    elif action == 'detail_user':
        return render_template('project_users.html', project=project)
    elif action == 'create_user':
        return render_template('create_user.html', project=project)
    elif action == 'create_tasks':
        return render_template('create_task.html', project=project)
    elif action == None:
        tasks = Task.query.all()
        volunteers = Volunteer.query.all()    
        return render_template('detail_project_view.html', tasks=tasks, volunteers=volunteers)
    else:
        abort(404)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
