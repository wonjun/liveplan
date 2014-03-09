import os

from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
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

DATABASE = 'sqlite:///%s/db/test.db'
DEBUG = True
SECRET_KEY = '\xf2v$@\xab\xbc\xfaw\x96\xbd\xa7~\x8f\xcc\xbaB\xe6\x82=9\x10&\x9b\xbe'
app.config['USERNAME'] = 'admin'
app.config['PASSWORD'] = 'default'


@app.route('/')
def home(admin=None):
    if 'logged_in' in session:
        return redirect(url_for('admin_dashboard'))
    else:
        return render_template('index.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    # look at models functions later to change
    projects = Project.query.all()
    return render_template('admin_dashboard.html', projects=projects)

@app.route('/admin_dashboard/create_project', methods=['GET', 'POST'])
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
            p = Project(request.form['name'], request.form['description'])
            db.session.add(p)
            db.session.commit()
            flash('You have successfully created a project!')
            return redirect(url_for('admin_dashboard')) # + project.id))
    return render_template('create_project.html', error=error)

@app.route('/admin_dashboard/<project>')
def project_page(project=None):
    tasks = Task.query.all()
    volunteers = Volunteer.query.all()
    return render_template('detail_project_view.html', tasks=tasks, volunteers=volunteers, project=project)

@app.route('/admin_dashboard/<project>/<detail_task>')
def detail_task(project=None, task=None):
    return render_template('project_tasks.html', project=project, task=task)

@app.route('/admin_dashboard/<project>/<detail_user>')
def detail_user(project=None, volunteer=None):
    return render_template('project_users.html', project=project, volunteer=volunteer)

@app.route('/admin_dashboard/<project>/create_user')
def create_user(project=None, methods=['GET', 'POST']):
    error = None
    if request.method == 'POST':
        if not request.form['name']:
            error = 'You do not have a name'
        elif not request.form['phone']:
            error = 'You do not have a phone'
        else:
            v = Volunteer(request.form['name'], request.form['phone'])
            db.session.add(v)
            db.session.commit()
            flash('You have successfully created a volunteer!')
            return redirect(url_for('admin_dashboard, project=project')) # + project.id))
    return render_template('create_user.html', error=error, pid=project)

@app.route('/admin_dashboard/<project>/create_task')
def create_task(project = None, methods=['GET', 'POST']):
    error = None
    print "GOT HERE"
    if request.method == 'POST':
        if not request.form['name']:
            error = 'You do not have a name'
        elif not request.form['start_time']:
            error = 'You do not have a start_time'
        elif not request.form['duration']:
            error = 'You do not have a duration'
        elif not request.form['short_description']:
            error = 'You do not have a short_description'
        elif not request.form['long_description']:
            error = 'You do not have a long_description'
        elif not request.form['max_volunteers']:
            error = 'You do not have a max_volunteers'
        else:
            t = Task(request.form['name'], request.form['start_time'], request.form['duration'], request.form['short_description'], request.form['long_description'], request.form['max_volunteers'])
            db.session.add(t)
            db.session.commit()
            flash('You have successfully created a task!')
            return redirect(url_for('admin_dashboard, project=project')) # + project.id))
    return render_template('create_task.html', error=error, pid=project)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if 'logged_in' in session:
        flash('You are already logged in')
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid Username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('admin_dashboard'))
    return render_template('index.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home'))

app.secret_key = SECRET_KEY

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
    db.engine.execute('DELETE FROM assignment WHERE task_id=%s AND volunteer_id=%s' % (str(task_id), str(volunteer_id)))
    db.session.commit()
    rows = db.engine.execute('SELECT * FROM assignment WHERE task_id=%s' % str(task_id))
    if not rows.scalar():
        db.engine.execute('UPDATE task SET completed=1 WHERE id=%s' % str(task_id))
        db.session.commit()

def accept_task(volunteer_id, task_id):
    # add task with 'id' to list of assigned tasks
    t = models.Task.query.get(task_id)
    db.engine.execute('INSERT INTO assignment VALUES (%s, %s)' % (str(task_id), str(volunteer_id)))
    db.session.commit()
    return t

def reject_task(volunteer_id, task_id):
    # reject task with 'id'
    return None

def more_task(task_id):
    return models.Task.query.get(task_id)

def get_user_by_phone(phone):
    return models.Volunteer.query.filter(models.Volunteer.phone==phone).first()

def list_project_volunteers(project_id):
    return models.Volunteer.query.filter(models.Volunteer.project_id==project_id).all()

def list_project_tasks(project_id):
    return models.Task.query.filter(models.Task.project_id==project_id).all()

def open_tasks(project_id):
    rows = db.engine.execute('select t.id, t.task_name, t.short_description from task t left join assignment a on t.id=a.task_id where t.project_id=%s EXCEPT select t.id, t.task_name, t.short_description from task t join assignment a on t.id=a.task_id where t.project_id=%s;' % (str(project_id), str(project_id)))
    return rows.fetchall()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
