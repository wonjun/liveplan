CREATE TABLE project (
	id INTEGER NOT NULL,
	name VARCHAR(80) NOT NULL,
	description TEXT,
	PRIMARY KEY (id)
);
CREATE TABLE task (
	id INTEGER NOT NULL,
	task_name VARCHAR(160) NOT NULL,
	project_id INTEGER NOT NULL,
	start_time TIMESTAMP NOT NULL,
	duration INTEGER NOT NULL,
	short_description VARCHAR(160),
	long_description TEXT,
	max_volunteers INTEGER NOT NULL,
	completed BOOLEAN NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(project_id) REFERENCES project (id),
	CHECK (completed IN (0, 1))
);
CREATE TABLE volunteer (
	id INTEGER NOT NULL,
	project_id INTEGER NOT NULL,
	name VARCHAR(40) NOT NULL,
	phone VARCHAR(15) NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(project_id) REFERENCES project (id),
	UNIQUE (phone)
);
CREATE TABLE assignment (
	task_id INTEGER,
	volunteer_id INTEGER,
	FOREIGN KEY(task_id) REFERENCES task (id),
	FOREIGN KEY(volunteer_id) REFERENCES volunteer (id)
);
