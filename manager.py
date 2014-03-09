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
    for i in range(4):
        p = Project(name='Project #%s' % str(i), description='Great description of this project')
        db.session.add(p)
        # Create Tasks for this Project
        for j in range(5):
            t = Task(task_name='Task #%s' % str(j), project_id=p, start_time=(dt+td), duration=TASK_DURATION,
                    short_description='Short description', long_description='This is a very long description',
                    max_volunteers=5)
            db.session.add(t)
            dt = dt + td
        # Create Volunteers for this Project
        tasks = [Task.query.filter_by(project_id=p).first()]
        print '======================='
        print tasks
        for j in range(5):
            v = Volunteer(project_id=p, name='Superstar Volunteer #%s' % str(j), phone='123-456-7890', tasks=tasks)
            db.session.add(v)
    db.session.commit()
