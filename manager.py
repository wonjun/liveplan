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
    p1 = Project(name='Social Good Hackathon', description="Wow this is the greatest hackathon I've ever been to")
    db.session.add(p1)
    p2 = Project(name='Social Bad Hackathon', description="Don't go to this one guys")
    db.session.add(p2)
    p3 = Project(name='Save the Squirrels', description="So many papers I don't have enough time to save the squirrels")
    db.session.add(p3)
    db.session.commit()
    # Create Tasks for this Project
    t1 = Task(task_name='Get tables from Cory', project_id=p1.id, start_time=(dt+td), duration=TASK_DURATION,
            short_description="Don't get lost guys", long_description='Please dont get lost',
            max_volunteers=5)
    db.session.add(t1)
    dt = dt + td
    t2 = Task(task_name='Get food from soda', project_id=p1.id, start_time=(dt+td), duration=TASK_DURATION,
            short_description='Hungry students are here', long_description='Hunger hunger hunger hunger',
            max_volunteers=5)
    db.session.add(t2)
    dt = dt + td
    t3 = Task(task_name='Clean Up', project_id=p1.id, start_time=(dt+td), duration=TASK_DURATION,
            short_description='This hackathon was so wild', long_description='Help please',
            max_volunteers=5)
    db.session.add(t3)
    dt = dt + td
    t4 = Task(task_name='SAVE ALL THE SQUIRRELS', project_id=p3.id, start_time=(dt+td), duration=TASK_DURATION,
            short_description='Please', long_description="It's a very real problem",
            max_volunteers=5)
    db.session.add(t4)
    dt = dt + td
    db.session.commit()
    # Create Volunteers for this Project
    v1 = Volunteer(project_id=p1.id, name='Kevin Gong', phone='+14438252032', tasks=[t1, t2, t3])
    db.session.add(v1)
    v2 = Volunteer(project_id=p1.id, name='Vincent Tian', phone='+15102464486', tasks=[t2, t3])
    db.session.add(v2)
    v3 = Volunteer(project_id=p3.id, name='Atsu Kakitani', phone='+16199470289', tasks=[t4])
    db.session.add(v3)
    v4 = Volunteer(project_id=p2.id, name='Wonjun Jeong', phone='+16192404050', tasks=[])
    db.session.add(v4)
    db.session.commit()
    db.session.remove()
