import sqlite3

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def db_table_create(conn):

    if conn is not None:
        sql_table = """
            CREATE TABLE IF NOT EXISTS kind (
                    id integer PRIMARY KEY AUTOINCREMENT,
                    kind_name varchar,
                    kind_location varchar,
                    food_type varchar
            );"""
        create_table(conn, sql_table)
        sql_table = """
            CREATE TABLE IF NOT EXISTS animal (
                    id integer PRIMARY KEY AUTOINCREMENT,
                    animal_name varchar,
                    gender varchar,
                    age integer,
                    kind_id integer,
                    food_amount integer,
                    FOREIGN KEY (kind_id) REFERENCES kind (id)
            );"""
        create_table(conn, sql_table)
        sql_table = """
            CREATE TABLE IF NOT EXISTS feeding (
                    animal_id integer,
                    employee_id integer,
                    feeding_day DATE,
                    feeding_time TIME,
                    FOREIGN KEY (animal_id) REFERENCES animal (id),
                    FOREIGN KEY (employee_id) REFERENCES employee (id)
            );"""
        
        create_table(conn, sql_table)
        sql_table = """
            CREATE TABLE IF NOT EXISTS  employee (
                    id integer PRIMARY KEY AUTOINCREMENT,
                    first_name varchar,
                    second_name varchar,
                    age integer,
                    experience integer
            );"""
        create_table(conn, sql_table)
    else:
        print("Ошибка\n")

def db_table_insert(conn):
    if conn is not None:
        sql_table = """
            INSERT OR IGNORE INTO kind(
                        id, kind_name, kind_location, food_type)
                VALUES (1, 'elephant', 'Africa', 'vegetables');"""
        create_table(conn, sql_table)
        conn.commit()

        sql_table = """
            INSERT OR IGNORE INTO kind(
                    id, kind_name, kind_location, food_type)
            VALUES (2, 'tiger', 'China', 'meat');"""
        create_table(conn, sql_table)
        conn.commit()

        sql_table = """
            INSERT OR IGNORE INTO kind(
                    id, kind_name, kind_location, food_type)
            VALUES (3, 'bear', 'Russia', 'meat');"""
        create_table(conn, sql_table)
        conn.commit()

        sql_table = """
            INSERT OR IGNORE INTO kind(
                    id, kind_name, kind_location, food_type)
            VALUES (4, 'leopard', 'Africa', 'meat');"""
        create_table(conn, sql_table)
        conn.commit()

        sql_table = """
            INSERT OR IGNORE INTO employee(
                    id, first_name, second_name, age, experience)
            VALUES (1, 'Jim', 'Pickens', 37, 7);"""
        create_table(conn, sql_table)
        conn.commit()

        sql_table = """
            INSERT OR IGNORE INTO employee(
                    id, first_name, second_name, age, experience)
            VALUES (2, 'Lora', 'Palmer', 23, 1);""" 
        create_table(conn, sql_table)
        conn.commit()

        sql_table = """
            INSERT OR IGNORE INTO animal(
                    id, animal_name, gender, age, kind_id, food_amount)
            VALUES (1, 'Lois', 'female', 3, 1, 10);"""
        create_table(conn, sql_table)
        conn.commit()

        sql_table = """
            INSERT OR IGNORE INTO animal(
                    id, animal_name, gender, age, kind_id, food_amount)
            VALUES (2, 'Rajah', 'male', 5, 2, 10);"""
        create_table(conn, sql_table)
        conn.commit()

        sql_table = """
            INSERT OR IGNORE INTO animal(
                    id, animal_name, gender, age, kind_id, food_amount)
            VALUES (3, 'Misha', 'male', 2, 3, 8);"""
        create_table(conn, sql_table)
        conn.commit()

        sql_table = """
            INSERT OR IGNORE INTO animal(
                    id, animal_name, gender, age, kind_id, food_amount)
            VALUES (4, 'Joan', 'female', 2, 4, 7);"""
        create_table(conn, sql_table)
        conn.commit()

        sql_table = """
            INSERT INTO feeding(
                    animal_id, employee_id, feeding_day, feeding_time)
            SELECT 1,1, '2019-01-01', '12:00'
            EXCEPT
            SELECT animal_id, employee_id, feeding_day, feeding_time
            FROM feeding
            WHERE
            animal_id = 1 AND employee_id = 1 AND feeding_day = '2019-01-01' AND feeding_time = '12:00'
            ;"""
        create_table(conn, sql_table)
        conn.commit()

        sql_table = """
            INSERT INTO feeding(
                    animal_id, employee_id, feeding_day, feeding_time)
            SELECT 4,1, '2019-01-01', '13:00'
            EXCEPT
            SELECT animal_id, employee_id, feeding_day, feeding_time
            FROM feeding
            WHERE
            animal_id = 4 AND employee_id = 1 AND feeding_day = '2019-01-01' AND feeding_time = '13:00';"""
        create_table(conn, sql_table)
        conn.commit()

        sql_table = """  
            INSERT INTO feeding(
                    animal_id, employee_id, feeding_day, feeding_time)
            SELECT 2,2, '2019-01-01', '12:30'
            EXCEPT
            SELECT animal_id, employee_id, feeding_day, feeding_time
            FROM feeding
            WHERE
            animal_id = 2 AND employee_id = 2 AND feeding_day = '2019-01-01' AND feeding_time = '12:30';"""
        create_table(conn, sql_table)
        conn.commit()

        sql_table = """
            INSERT INTO feeding(
                    animal_id, employee_id, feeding_day, feeding_time)
            SELECT 3,2, '2019-01-01', '13:30'
            EXCEPT
            SELECT animal_id, employee_id, feeding_day, feeding_time
            FROM feeding
            WHERE
            animal_id = 3 AND employee_id = 2 AND feeding_day = '2019-01-01' AND feeding_time = '13:30';"""
        create_table(conn, sql_table)
        conn.commit()

#db_table_create()
#db_table_insert()



