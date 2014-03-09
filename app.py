import os

from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy
from models import *
from twilio_api import send_text
import twilio.twiml
from datetime import datetime

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

def list_project_volunteers(project_id):
    all_volunteers = db.session.query(models.Volunteer).filter(models.Volunteer.project_id==project_id).all()
    avail_volunteers = []
    for vol in all_volunteers:
        print vol
        if len(list_tasks(vol.id)) == 0:
            avail_volunteers.append(vol)
    return db.session.query(models.Volunteer).filter(models.Volunteer.project_id==project_id).all()

def list_project_tasks(project_id):
    return db.session.query(models.Task).filter(models.Task.project_id==project_id).all()

@app.route('/admin_dashboard')
def admin_dashboard():
    # look at models functions later to change
    projects = db.session.query(models.Project).all()
    data = {}
    for project in projects:
        data[project] = [list_project_tasks(project.id), list_project_volunteers(project.id)]
    return render_template('admin_dashboard.html', data=data)

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
    tasks = db.session.query(models.Task).all()
    volunteers = db.session.query(models.Volunteer).all()
    return render_template('detail_project_view.html', tasks=tasks, volunteers=volunteers, project=project)

@app.route('/admin_dashboard/<project>/detail_task')
def detail_task(project=None, task=None):
    tasks = list_project_tasks(project)
    return render_template('project_tasks.html',tasks=tasks)

@app.route('/admin_dashboard/<project>/detail_user')
def detail_user(project=None, volunteer=None):
    volunteers = list_project_volunteers(project)
    return render_template('project_users.html', volunteers=volunteers)

@app.route('/admin_dashboard/<project>/create_user', methods=['GET', 'POST'])
def create_user(project=None):
    error = None
    print request.method
    if request.method == 'POST':
        if not request.form['name']:
            error = 'You do not have a name'
        elif not request.form['phone']:
            error = 'You do not have a phone'
        else:
            v = Volunteer(project, request.form['name'], request.form['phone'], [])
            db.session.add(v)
            db.session.commit()
            flash('You have successfully created a volunteer!')
            return redirect(url_for('admin_dashboard')) # + project.id))
    return render_template('create_user.html', error=error, pid=project)

@app.route('/admin_dashboard/<project>/create_task', methods=['GET', 'POST'])
def create_task(project = None):
    error = None
    print request.method
    if request.method == 'POST':
        if not request.form['task_name']:
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
            # handle datetime object
            date_object = datetime.strptime(request.form['start_time'], '%b %d %Y %I:%M%p')
            t = Task(request.form['task_name'], project, date_object, request.form['duration'], request.form['short_description'], request.form['long_description'], request.form['max_volunteers'], False)
            db.session.add(t)
            db.session.commit()
            message = "New task, " + str(t.task_name) + " (" + str(t.id) + "), at " + str(t.start_time) + "for " + str(t.max_volunteers)
            for volunteer in list_project_volunteers(project):
                twilio.send_text(volunteer.phone, twilio_api.FROM_NUMBER, message)
            flash('You have successfully created a task!')
            return redirect(url_for('admin_dashboard')) # + project.id))
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

def parse_received_texts(from_number, received_text):
    parsed_received_text = received_text.split()
    print "==============="
    print parsed_received_text[0]
    volunteer = get_user_by_phone(from_number)
    resp = twilio.twiml.Response()
    response = None
    if len(parsed_received_text) == 1:
        if parsed_received_text[0] == 'list':
            tasks = list_tasks(volunteer.id)
            for task in tasks:
                response += task.id + ": " + task.task_name + " - " + task.start_time + "\n"
        elif parsed_received_text[0] == 'available':
            for (task_name, task_id, task_short) in open_tasks(volunteer.project_id):
                response += task_name + "(" + task_id + "): " + task_short + "\n"
        else:
            response = parsed_received_text[0]
    elif len(parsed_received_text) == 2:
        print "====== length 2 ======="
        command = parsed_received_text[0]
        task_id = int(parsed_received_text[1])
        print "===== " + str(task_id) + " ======="
        task = more_task(task_id)
        if task == None:
            response = 'Invalid Command2'
        elif command == 'finish':
            print "====== finish ======="
            finish_task(volunteer.id, task_id)
            response = 'Task successfully completed.'
        elif command == 'accept':
            print "====== accept ======="
            accept_task(volunteer.id, task_id)
            response = 'Task successfully accepted.'
        elif command == 'reject':
            print "====== reject ======="
            response = 'Rejected task.'
            pass
        elif command == 'more':
            print "====== more ======="
            response = task.task_name + ": " + task.short_description + "\n"
            response += task.long_description
        else:
            response = 'Invalid Command3'
    else:
        response = 'Invalid Command4'
    resp.message(response)
    return str(resp)

@app.route("/receive_text", methods=['GET', 'POST'])
def receive_text():
    from_number = str(request.values.get('From', None))
    message = str(request.values.get('Body', None))
    return parse_received_texts(from_number, message)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

def list_tasks(volunteer_id):
    # 'list' all current tasks for volunteer
    return db.session.query(models.Volunteer).get(volunteer_id).tasks

def finish_task(volunteer_id, task_id):
    # mark task with 'id' as finished
    db.engine.execute('DELETE FROM assignment WHERE task_id=%s AND volunteer_id=%s' % (str(task_id), str(volunteer_id)))
    db.session.commit()
    rows = db.engine.execute('SELECT * FROM assignment WHERE task_id=%s' % str(task_id))
    if not rows.scalar():
        true_boolean = 1
        if IS_HEROKU:
            true_boolean = True
        db.engine.execute('UPDATE task SET completed=%s WHERE id=%s' % (str(true_boolean), str(task_id)))
        db.session.commit()

def accept_task(volunteer_id, task_id):
    # add task with 'id' to list of assigned tasks
    t = db.session.query(models.Task).get(task_id)
    db.engine.execute('INSERT INTO assignment VALUES (%s, %s)' % (str(task_id), str(volunteer_id)))
    db.session.commit()
    return t

def reject_task(volunteer_id, task_id):
    # reject task with 'id'
    return None

def more_task(task_id):
    return db.session.querymodels.Task().get(task_id)

def get_user_by_phone(phone):
    return db.session.query(models.Volunteer).filter(models.Volunteer.phone==phone).first()

def open_tasks(project_id):
    rows = db.engine.execute('select t.id, t.task_name, t.short_description from task t left join assignment a on t.id=a.task_id where t.project_id=%s EXCEPT select t.id, t.task_name, t.short_description from task t join assignment a on t.id=a.task_id where t.project_id=%s;' % (str(project_id), str(project_id)))
    return rows.fetchall()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
