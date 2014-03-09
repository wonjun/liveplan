import datetime

from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, Text
from database import Base, engine
from app import db

class Project(Base):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(Text)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return "Project name: " + self.name


tasks = db.Table('assignment', Base.metadata,
    db.Column('task_id', Integer, ForeignKey('task.id')),
    db.Column('volunteer_id', Integer, ForeignKey('volunteer.id'))
)


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task_name = Column(String(160), nullable=False)
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False)
    start_time = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False)
    short_description = Column(String(160))
    long_description = Column(Text)
    max_volunteers = Column(Integer, nullable=False)

    def __init__(self, task_name, project_id, start_time, duration, short_description, long_description, max_volunteers):
        self.task_name = task_name
        self.project_id = project_id
        self.start_time = start_time
        self.duration = duration
        self.short_description = short_description
        self.long_description = long_description
        self.max_volunteers = max_volunteers

    def __repr__(self):
        return self.task_name + "'s description: " + self.short_description

    @property
    def end_time(self):
        return self.start_time + datetime.timedelta(minutes=self.duration)


class Volunteer(Base):
    __tablename__ = 'volunteer'
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False)
    name = Column(String(40), nullable=False)
    phone = Column(String(15), nullable=False)
    tasks = db.relationship('Task', secondary=tasks, backref='volunteers')

    def __init__(self, project_id, name, phone, tasks):
        self.project_id = project_id
        self.name = name
        self.phone = phone
        self.tasks = tasks

    def __repr__(self):
        return "Volunteer name: " + self.name + "Phone Number: " + self.phone

    def is_busy(self):
        return False
