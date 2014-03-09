import datetime
import os

from flask import Flask
from flask import render_template
from flask.ext.sqlalchemy import SQLAlchemy

from models import Project, Volunteer, Task


IS_HEROKU = 'IS_HEROKU' in os.environ

app = Flask(__name__)
if IS_HEROKU:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s/db/test.db' % os.path.dirname(os.path.realpath(__file__))
db = SQLAlchemy(app)

TASK_STEP = 60
TASK_DURATION = 30

def seed():
    "Add seed data to the database."
    dt = datetime.datetime(2014, 3, 9)
    td = datetime.timedelta(minutes=TASK_STEP)
    # Create Projects
    #for i in range(4):
    p1 = Project(name='Project #%s' % str(1), description='Great description of this project')
    db.session.add(p1)
    p2 = Project(name='Project #%s' % str(2), description='Great description of this project')
    db.session.add(p2)
    p3 = Project(name='Project #%s' % str(3), description='Great description of this project')
    db.session.add(p3)
    db.session.commit()
    # Create Tasks for this Project
    t1 = Task(task_name='Task #%s' % str(1), project_id=p1.id, start_time=(dt+td), duration=TASK_DURATION,
            short_description='Short description', long_description='This is a very long description',
            max_volunteers=5)
    db.session.add(t1)
    dt = dt + td
    t2 = Task(task_name='Task #%s' % str(2), project_id=p1.id, start_time=(dt+td), duration=TASK_DURATION,
            short_description='Short description', long_description='This is a very long description',
            max_volunteers=5)
    db.session.add(t2)
    dt = dt + td
    t3 = Task(task_name='Task #%s' % str(3), project_id=p1.id, start_time=(dt+td), duration=TASK_DURATION,
            short_description='Short description', long_description='This is a very long description',
            max_volunteers=5)
    db.session.add(t3)
    dt = dt + td
    t = Task(task_name='Task #%s' % str(1), project_id=p2.id, start_time=(dt+td), duration=TASK_DURATION,
            short_description='Short description', long_description='This is a very long description',
            max_volunteers=5)
    db.session.add(t)
    dt = dt + td
    db.session.commit()
    # Create Volunteers for this Project
    tasks = Task.query.filter_by(project_id=p1.id).all()
    v = Volunteer(project_id=p1.id, name='Superstar Volunteer #%s' % str(1), phone='123-456-7890', tasks=[t1, t2, t3])
    db.session.add(v)
    db.session.commit()
    db.session.remove()
