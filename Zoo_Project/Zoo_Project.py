# -*- coding: utf-8 -*-
import sqlite3
import sys
import create_table
import json
import datetime
from prettytable import PrettyTable

def type_selection():
    k = input("Тип питания:\n1. Травоядное\n2. Плотоядное\n3. Всеядное\n")
    while int_check(k) is False or (int(k) > 3) or (int(k) < 1):
        k = input()
    return  int(k)

def time_check(time_text):
    try:
        datetime.datetime.strptime(time_text, '%H:%M')
    except:
        print ("Неправильно введено время")
        return False
    return True

def date_check(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        print ("Неправильно введена дата")
        return False
    return True

def int_check(is_int):
    try:
        is_int = int(is_int)
    except:
        print("Неправильно введено число\n")
        return False
    return True

def animal_choice():
    che = False
    while (che is False):
        print("Выберите животное: \n")
        c.execute('SELECT * FROM animal')
        row = c.fetchone()
        while row is not None:
           print("id: "+str(row[0])+" - "+row[1])
           row = c.fetchone()
        an_id = input()
        che = int_check(an_id)
    return an_id

def employee_choice():
    che = False
    while (che is False):
        print("Выберите работника: \n")
        c.execute('SELECT * FROM employee')
        row = c.fetchone()
        while row is not None:
           print("id: "+str(row[0])+" - "+row[1])
           row = c.fetchone()
        emp_id = input()
        che = int_check(emp_id)
    return emp_id

def food_choice(an_food_type):
    che = False
    while che is False:
        print("Выберите продукт: \n")
        c.execute('SELECT id, food_name FROM food')
        row = c.fetchone()
        while row is not None:
           print("id: "+str(row[0])+" - "+row[1])
           row = c.fetchone()
        f_id = input()
        che = int_check(f_id)
    c.execute("SELECT type FROM food WHERE id = ?", (f_id,))
    k = c.fetchone()
    food_type = k[0]
    an_food_type = int(an_food_type)
    if (an_food_type == 1 and food_type == 1) or (an_food_type == 3) or (an_food_type == 2 and food_type == 2):
        return f_id
    else:
        return -1

def add_food():
    name = input("Введите название продукта:\n")
    t = input("Тип питания:\n1. Для травоядных\n2. Для плотоядных\n3. Для всеядных\n")
    while int_check(t) is False or (int(t) > 3) or (int(t) < 1):
        t = input()
    st = input("Сколько продукта на складе? (в кг)\n")
    if int_check(st) is False:
        return
    check.execute("SELECT * FROM food WHERE food_name = ?" , (str(name),))
    row = check.fetchone()
    if (row is None):
        c.execute("INSERT INTO food(food_name, in_storage, type)VALUES('%s', %s, %s)"%(name, int(st), t))
        conn.commit()
    else:
        ch = input("Такой продукт уже есть в списке, хотите обновить количество продукта в хранилище на введенное?\n1. Да \n2. Нет\n")
        if int(ch) == 1:
            c.execute ("UPDATE food SET in_storage = ? WHERE food_name = ?", (int(st), name,))
            conn.commit()
        else:
            return

def add_employee():
    first_name = input("Имя: \n")
    second_name = input("Фамилия: \n")
    age = input("Возраст: \n")
    if int_check(age) is False:
        return
    experience = input("Опыт работы: \n")
    if int_check(experience) is False:
        return
    #checking if employee already exists
    check.execute("SELECT * FROM employee WHERE first_name = ? AND second_name = ? AND age = ? AND experience = ?" , (str(first_name), str(second_name), str(age), str(experience),))
    row = check.fetchone()
    if (row is None):
        c.execute("INSERT INTO employee(first_name, second_name, age, experience)VALUES('%s', '%s', %s, %s)"%(first_name, second_name, age, experience))
        conn.commit()
    else:
        print("Такой работник уже есть в списке\n") 

def add_kind():
    kind_name = input("Название вида: \n")
    kind_location = input("Местоположение вида: \n")
    food_type = type_selection()
    if int_check(food_type) is False:
        return

    #checking if kind already exists
    check.execute("SELECT * FROM kind WHERE kind_name = ? AND kind_location = ?" , (str(kind_name), str(kind_location),))
    row = check.fetchone()
    if row is None:
        c.execute("INSERT INTO kind(kind_name, kind_location, type)VALUES('%s', '%s', %s)"%(kind_name, kind_location, food_type))
        conn.commit()
    else:
        print("Такой вид уже есть в списке\n")
        
def add_animal():
    animal_name = input("Имя: \n")
    gender = input("Пол (male/female): \n")
    if (str(gender) != "male") and (str(gender) != "female"):
        print("Введены неверные данные")
        return
    age = input("Возраст: \n")
    if int_check(age) is False:
        return
    
    print("Вид животного (id): ")
    c.execute('SELECT id, kind_name FROM kind')
    row = c.fetchone()
    while row is not None:
        print("id: "+str(row[0])+" - "+row[1]+"\n")
        row = c.fetchone()
    print   ("    0 - Добавить новый вид животного")
    choice = input()
    if int_check(choice) is False:
        return
    choice = int(choice)
    if (choice == 0):
        add_kind()
        c.execute('SELECT * FROM kind')
        row = c.fetchone()
        while row is not None:
            last = int(row[0])
            row = c.fetchone()
        kind_id = last
    else:
        kind_id = choice
        
    #checking if animal already exists
    check.execute("SELECT * FROM animal WHERE animal_name = ? AND gender = ? AND age = ? AND kind_id = ?" , (str(animal_name), str(gender), str(age), str(kind_id),))
    row = check.fetchone()
    if row is None:
        c.execute("INSERT INTO animal (animal_name, gender, age, kind_id)VALUES('%s', '%s', %s, %s)"%(animal_name, gender, age, int(kind_id)))
        conn.commit()
    else:
        print ("Такое животное уже есть в списке\n")

def add_feeding():
    animal_id = animal_choice()
    employee_id = employee_choice()
    
    feeding_day = input("Введите дату в формате YYYY-MM-DD: \n")
    if (date_check(feeding_day) is False):
        return
    feeding_time = input("Введите время в формате HH:MM\n")
    if (time_check(feeding_time) is False):
        return
    c.execute("SELECT kind.type FROM kind INNER JOIN animal ON animal.kind_id = kind.id AND animal.id = ?", (animal_id,))
    row = c.fetchone()
    food_id = food_choice(row[0])

    if food_id == -1:
        print ("Для этого животного выбран неподходящий тип питания")
        return
    c.execute("SELECT in_storage FROM food WHERE food.id = ?", (food_id,))
    row = c.fetchone()
    food_amount = input("Введите количество продукта\n")
    if int_check(food_amount) is False:
        return
    if (int(food_amount) > int(row[0])):
        print ("В хранилище нет такого количества этого продукта")
        return
    minus_storage(food_id, food_amount)
    
    #checking if record already exists
    query = "SELECT * FROM feeding WHERE employee_id = ? AND feeding_day = ? AND feeding_time = ?"
    check.execute(query , (str(employee_id), str(feeding_day), str(feeding_time),))
    row = check.fetchone()
    if row is not None:
        print ("Такая запись в расписании уже существует")
        return
    
    query = "SELECT * FROM feeding WHERE animal_id = ? AND feeding_day = ? AND feeding_time = ?"
    check.execute(query , (str(animal_id), str(feeding_day), str(feeding_time),))
    row = check.fetchone()
    if row is not None:
        print ("Такая запись в расписании уже существует")
        return
    #everything is ok
    c.execute("INSERT INTO feeding(animal_id, employee_id, feeding_day, feeding_time, food_amount, food_id)VALUES(%s, %s, '%s', '%s', '%s', '%s')"%(animal_id, employee_id, feeding_day, feeding_time, food_amount, food_id))
    conn.commit()

def table_out():
    choise = int(input("1. Список животных в зоопарке \n2. Список работников зоопарка \n3. Количество еды в хранилище\n4. Расписание для кормления животных\n5. Закрыть\n"))
    #   animal table
    if (choise == 1):
        x = PrettyTable()
        x.field_names = ["Имя животного", "Пол", "Возраст", "Вид"]
        c.execute('SELECT * FROM animal')
        row = c.fetchone()
        while row is not None:
            name = row[1]
            sex = row[2]
            age = str(row[3])
            kind_id = int(row[4])
            n.execute("SELECT kind_name FROM kind WHERE id = ?", (kind_id,))
            k = n.fetchone()
            kind_name = str(k[0])
            x.add_row([name, sex, age, kind_name])
            row = c.fetchone()
        print(x)
    #   employee table    
    elif (choise == 2):
        x = PrettyTable()
        x.field_names = ["Имя", "Фамилия", "Возраст", "Опыт работы"]
        c.execute('SELECT * FROM employee')
        row = c.fetchone()
        while row is not None:
            name = row[1]
            fam_name = row[2]
            age = str(row[3])
            expi = str(row[4])
            x.add_row([name, fam_name, age, expi])
            row = c.fetchone()
        print(x)
    elif choise == 3:
        x = PrettyTable()
        x.field_names = ["Название продукта", "Количество"]
        c.execute('SELECT food_name, in_storage FROM food')
        row = c.fetchone()
        while row is not None:
            x.add_row([row[0], row[1]])
            row = c.fetchone()
        print(x)
    #   schedules
    elif (choise == 4):
        ch = int(input("1. Все расписание \n2. Расписание для нужного животного \n3. Расписание для работника \n4. Расписание на день \n5. Закрыть\n"))
        if (ch == 1):
            feeding_schedule()
        elif (ch == 2):
            feeding_animal()
        elif (ch == 3):
            feeding_employee()
        elif (ch == 4):
            feeding_day()
        else:
            return
    #   exit menu
    else:
        return

def feeding_animal():
    an_id = animal_choice()
    query = """SELECT employee.first_name, employee.second_name, animal.animal_name, kind.kind_name, 
                food.food_name, feeding.food_amount, feeding.feeding_day, feeding.feeding_time, feeding.if_done 
               FROM feeding 
               INNER JOIN animal ON animal.id = feeding.animal_id
               INNER JOIN kind ON animal.kind_id = kind.id     
               INNER JOIN food ON feeding.food_id = food.id
               INNER JOIN employee ON employee.id = feeding.employee_id
               WHERE animal_id = ?
               ORDER BY feeding_day, feeding_time"""
    c.execute(query, (an_id,))
    x = PrettyTable()
    x.field_names = ["Имя работника", "Фамилия работника", "Имя животного", "Вид животного", "Продукт", "Количество еды (в кг)", "Дата кормления", "Время кормления", "Сделано"]
    row = c.fetchone()
    while row is not None:
        x.add_row([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]])
        row = c.fetchone()
    print(x)
    
def feeding_employee():
    emp_id = employee_choice()
    query = """SELECT employee.first_name, employee.second_name, animal.animal_name, kind.kind_name, 
                food.food_name, feeding.food_amount, feeding.feeding_day, feeding.feeding_time, feeding.if_done  
               FROM feeding 
               INNER JOIN animal ON animal.id = feeding.animal_id
               INNER JOIN kind ON animal.kind_id = kind.id     
               INNER JOIN food ON feeding.id = food.id
               INNER JOIN employee ON employee.id = feeding.employee_id
               WHERE employee_id = ?
               ORDER BY feeding_day, feeding_time"""
    c.execute(query, (emp_id,))
    x = PrettyTable()
    x.field_names = ["Имя работника", "Фамилия работника", "Имя животного", "Вид животного", "Продукт", "Количество еды (в кг)", "Дата кормления", "Время кормления", "Сделано"]
    row = c.fetchone()
    while row is not None:
        x.add_row([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]])
        row = c.fetchone()
    print(x)

def feeding_day():
    an_date = input("Введите дату в формате YYYY-MM-DD\n")
    if date_check(an_date) is False:
        return
    query = """SELECT employee.first_name, employee.second_name, animal.animal_name, kind.kind_name, 
                food.food_name, feeding.food_amount, feeding.feeding_day, feeding.feeding_time, feeding.if_done  
               FROM feeding 
               INNER JOIN animal ON animal.id = feeding.animal_id
               INNER JOIN kind ON animal.kind_id = kind.id     
               INNER JOIN food ON feeding.food_id = food.id
               INNER JOIN employee ON employee.id = feeding.employee_id
               WHERE feeding_day = ?
               ORDER BY feeding_day, feeding_time"""
    c.execute(query, (an_date,))
    x = PrettyTable()
    x.field_names = ["Имя работника", "Фамилия работника", "Имя животного", "Вид животного", "Продукт", "Количество еды (в кг)", "Дата кормления", "Время кормления", "Сделано"]
    row = c.fetchone()
    while row is not None:
        x.add_row([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]])
        row = c.fetchone()
    print(x)
    
def feeding_schedule():
    query = """SELECT employee.first_name, employee.second_name, animal.animal_name, kind.kind_name, 
                food.food_name, feeding.food_amount, feeding.feeding_day, feeding.feeding_time, feeding.if_done 
               FROM feeding 
               INNER JOIN animal ON animal.id = feeding.animal_id
               INNER JOIN kind ON animal.kind_id = kind.id     
               INNER JOIN food ON feeding.food_id = food.id
               INNER JOIN employee ON employee.id = feeding.employee_id
               ORDER BY feeding_day, feeding_time"""
    c.execute(query)
    x = PrettyTable()
    x.field_names = ["Имя работника", "Фамилия работника", "Имя животного", "Вид животного", "Продукт", "Количество еды (в кг)", "Дата кормления", "Время кормления", "Сделано"]
    row = c.fetchone()
    while row is not None:
        x.add_row([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]])
        row = c.fetchone()
    print(x)

def table_in():
    choise = int(input("1. Добавить вид \n2. Добавить новое животное \n3. Добавить нового работника \n4. Добавить расписание кормления \n5. Добавить продукт\n6. Закрыть\n"))
    if (choise == 1):
        add_kind()
    elif (choise == 2):
        add_animal()
    elif (choise == 3):
        add_employee()
    elif (choise == 4):
        add_feeding()
    elif choise == 5:
        add_food()
    else:
        return

def to_json():
    f = open('zoo.json', 'w')
    
    query = """SELECT employee.first_name, employee.second_name, animal.animal_name, kind.kind_name, 
                food.food_name, feeding.food_amount, feeding.feeding_day, feeding.feeding_time, feeding.if_done 
               FROM feeding 
               INNER JOIN animal ON animal.id = feeding.animal_id
               INNER JOIN kind ON animal.kind_id = kind.id     
               INNER JOIN food ON feeding.food_id = food.id
               INNER JOIN employee ON employee.id = feeding.employee_id
               ORDER BY feeding_day, feeding_time"""
    result = c.execute(query)
    json_zoo = [dict(zip([key[0] for key in c.description], row)) for row in result]

    
    text = json.dumps({'zoo': json_zoo}, indent=4)
    f.write(text)
    f.close()

def check_when_done():
    query = """SELECT feeding.id, employee.first_name, employee.second_name, animal.animal_name, kind.kind_name, 
                food.food_name, feeding.food_amount, feeding.feeding_day, feeding.feeding_time, feeding.if_done 
               FROM feeding 
               INNER JOIN animal ON animal.id = feeding.animal_id
               INNER JOIN kind ON animal.kind_id = kind.id     
               INNER JOIN food ON feeding.food_id = food.id
               INNER JOIN employee ON employee.id = feeding.employee_id"""
    c.execute(query)
    x = PrettyTable()
    x.field_names = ["ID","Имя работника", "Фамилия работника", "Имя животного", "Вид животного", "Продукт", "Количество еды (в кг)", "Дата кормления", "Время кормления", "Сделано"]
    row = c.fetchone()
    while row is not None:
        x.add_row([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]])
        row = c.fetchone()
    print(x)

    ch = input("Введите ID события, которое было выполнено\n")
    if int_check(ch) is False:
        return
    query = """UPDATE feeding SET if_done = 1 WHERE id = ?"""
    c.execute(query, (ch,))
    conn.commit()
    

def minus_storage(food_id, amount):
    query = """ SELECT in_storage FROM food WHERE id = ?"""
    c.execute(query, (food_id,))
    k = c.fetchone()
    query = """ UPDATE food SET in_storage = ? WHERE id = ?"""
    c.execute (query, (int(k[0])-int(amount), food_id,))
    conn.commit()
        
database = "zoo_db.db"
try:
    conn = sqlite3.connect(database)
    c = conn.cursor()
    n = conn.cursor()
    check = conn.cursor()
except Error as e:
    print(e)

while True:
    choice = input("1. Ввести данные\n2. Вывести данные\n3. Отметить в расписании выполненным \n4. Закрыть программу\n")
    if int_check(choice) is False:
        break
    choice = int(choice)
    if choice == 1:
        table_in()
    elif choice == 2:
        table_out()
    elif choice == 3:
        check_when_done()
    else:
        break
  
to_json()
c.close()
n.close()
check.close()
conn.close()










