import os

from flask import Flask
from flask import render_template
from flask.ext.sqlalchemy import SQLAlchemy
from models import *
from twilio_api import send_text
import twilio.twiml

from database import db_session
import models

IS_HEROKU = 'IS_HEROKU' in os.environ

app = Flask(__name__)
if IS_HEROKU:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s/db/test.db' % os.path.dirname(os.path.realpath(__file__))
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


@app.route("/receive_text", methods=['GET', 'POST'])
def receive_text():
    from_number = request.values.get('From', None)
    message = request.values.get('Message', None)
    # call parse_received_texts(from_number, message)
    return

def parse_received_texts(from_number, received_text):
    parsed_received_text = received_text.split()
    if len(parsed_received_text) == 1:
        if parsed_received_text[0] == 'list':
            # list all current tasks
            response = 'list of tasks'
        elif parsed_received_text[0] == 'available':
            # list all non-assigned tasks sorted by priority
            response = 'list of available tasks'
        else:
            # invalid command
            response = 'invalid command'
    elif len(parsed_received_text) == 2:
        command = parsed_received_text[0]
        task_id = parsed_received_text[1]
        # if task_id does not exist:
            # fail
        resp = twilio.twiml.Response()
        if command == 'finish':
            response = 'woohoo!'
            # update server that task is done
        elif command == 'accept':
            # update server that user accepted task
            response = 'confirmation message'
        elif command == 'reject':
            response = 'ok :/'
            pass
        elif command == 'more':
            response = 'here is additional information'
            # give additional info on task
        else:
            # invalid command
            response = 'invalid command'
    else:
        # invalid command
        response = 'invalid command'
    resp.message(response)
    return str(resp)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


def list_tasks(volunteer_id):
    # 'list' all current tasks for volunteer
    return models.Volunteer.query.get(volunteer_id).tasks

def finish_task(volunteer_id, task_id):
    # mark task with 'id' as finished
    models.Volunteer.query.get(volunteer_id).tasks.remove(models.Task.query.get(task_id))
    db.commit()

def accept_task(volunteer_id, task_id):
    # add task with 'id' to list of assigned tasks
    t = models.Task.query.get(task_id)
    models.Volunteer.query.get(volunteer_id).tasks.add(models.Task.query.get(t))
    db.commit()
    return t

def reject_task(volunteer_id, task_id):
    # reject task with 'id'
    return None

def more_task(task_id):
    return models.Task.query.get(task_id)

