CREATE TABLE IF NOT EXISTS animal (
	id integer PRIMARY KEY AUTOINCREMENT,
	animal_name varchar,
	gender varchar,
	age integer,
	kind_id integer,
	FOREIGN KEY (kind_id) REFERENCES kind (id)
);

CREATE TABLE IF NOT EXISTS kind (
	id integer PRIMARY KEY AUTOINCREMENT,
	kind_name varchar,
	kind_location varchar,
	type varchar
);

CREATE TABLE IF NOT EXISTS feeding (
	id integer PRIMARY KEY AUTOINCREMENT,
	animal_id integer,
	employee_id integer,
	feeding_day DATE,
	feeding_time TIME,
	food_amount INTEGER,
	food_id INTEGER,
	if_done BOOLEAN DEFAULT 0,
	FOREIGN KEY (food_id) REFERENCES food (id),
	FOREIGN KEY (animal_id) REFERENCES animal (id),
	FOREIGN KEY (employee_id) REFERENCES employee (id)
);

CREATE TABLE IF NOT EXISTS food(
	id integer PRIMARY KEY AUTOINCREMENT,
	food_name varchar,
	in_storage integer,
	type integer
);

CREATE TABLE IF NOT EXISTS employee (
	id integer PRIMARY KEY AUTOINCREMENT,
	first_name varchar,
	second_name varchar,
	age integer,
	experience integer
);

