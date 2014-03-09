from flask import Flask
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from app import db

class Project(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(Text, unique=True)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return "Project name: " + self.name

class Task(db.Model):
    id = Column(Integer, primary_key=True)
    task_name = Column(String(160))
    project_id = Column(Integer, ForeignKey('project.id'))
    start_time = Column(DateTime)
    duration = Column(Integer)
    short_description = Column(String(160))
    long_description = Column(Text)
    max_volunteers = Column(Integer)

    def __init__(self, task_name, project_id, start_time, duration, short_description, long_description, max_volunteers):
        self.task_name = task_name
        self.project_id = project_id
        self.start_time = start_time
        self.duration = duration
        self.short_description = short_description
        self.long_description = long_description
        self.max_volunteer = max_volunteers

    def __repr__(self):
        return self.task_name + "'s description: " + self.short_description

class Volunteers(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(40), unique=True)
    phone = Column(String(15), unique=True)
    status = Column(Boolean, unique=True)

    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
        self.status = True

    def __repr__(self):
        return "Volunteer name: " + self.name + "Phone Number: " + self.phone
