INSERT INTO kind(
            id, kind_name, kind_location, type)
    VALUES (1, 'elephant', 'Africa', 1);

INSERT INTO kind(
            id, kind_name, kind_location, type)
    VALUES (2, 'tiger', 'China', 2);

INSERT INTO kind(
            id, kind_name, kind_location, type)
    VALUES (3, 'bear', 'Russia', 3);

INSERT INTO kind(
            id, kind_name, kind_location, type)
    VALUES (4, 'leopard', 'Africa', 2);



INSERT INTO employee(
            id, first_name, second_name, age, experience)
    VALUES (1, 'Jim', 'Pickens', 37, 7);

INSERT INTO employee(
            id, first_name, second_name, age, experience)
    VALUES (2, 'Lora', 'Palmer', 23, 1);    

    
    
INSERT INTO animal(
            id, animal_name, gender, age, kind_id)
    VALUES (1, 'Lois', 'female', 3, 1);

INSERT INTO animal(
            id, animal_name, gender, age, kind_id)
    VALUES (2, 'Rajah', 'male', 5, 2);

INSERT INTO animal(
            id, animal_name, gender, age, kind_id)
    VALUES (3, 'Misha', 'male', 2, 3);

INSERT INTO animal(
            id, animal_name, gender, age, kind_id)
    VALUES (4, 'Joan', 'female', 2, 4);


INSERT INTO food (
		 id, food_name, in_storage, type)
    VALUES (1, 'raw meat', 400, 2);

INSERT INTO food (
		 id, food_name, in_storage, type)
    VALUES (2, 'fish', 500, 2);

INSERT INTO food (
		 id, food_name, in_storage, type)
    VALUES (3, 'vegetables', 300, 1);

INSERT INTO food (
		 id, food_name, in_storage, type)
    VALUES (4, 'chicken meat', 200, 2);


INSERT INTO feeding( id,
            animal_id, employee_id, feeding_day, feeding_time, food_amount, food_id)
    VALUES (1,1,1, '2019-01-01', '12:00', 7, 3);

INSERT INTO feeding( id,
            animal_id, employee_id, feeding_day, feeding_time, food_amount, food_id)
    VALUES (2,4,1, '2019-01-01', '13:00', 5, 2);    

INSERT INTO feeding(id, 
		 animal_id, employee_id, feeding_day, feeding_time, food_amount, food_id)    
    VALUES (3,2,2, '2019-01-01', '12:30', 6, 4);

INSERT INTO feeding(id, 
            animal_id, employee_id, feeding_day, feeding_time, food_amount, food_id)
    VALUES (4,3,2, '2019-01-01', '13:30', 5, 1);