from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

class Project(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(Text, unique=True)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return "Project name: " + name 

class Task(db.Model):
    id = Column(Integer, primary_key=True)
    task_name = Column(String(160))
    project_id = Column(Integer, ForeignKey('project.id'))
    start_time = Column(DateTime)
    duration = Column(Integer)
    short_description = Column(String(160))
    long_description = Column(Text)
    max_volunteers = Column(Integer)

    def __init__(self, username, email):
        self.task_name = task_name
        self.project_id = project_id
        self.start_time = start_time
        self.duration = duration
        self.short_description = short_description
        self.long_description = long_description
        self.max_volunteer = max_volunteer

    def __repr__(self):
        return task_name + "'s description: " + short_description