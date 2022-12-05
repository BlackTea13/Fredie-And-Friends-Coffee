INSERT INTO city_country
VALUES
    ('bangkok', 'thailand'),
    ('phuket', 'thailand'),
    ('singapore', 'singapore'),
    ('pattaya', 'thailand');

INSERT INTO district_zip
VALUES
    ('winston', 10240),
    ('zarya', 10555),
    ('merlion', 80050),
    ('zenyatta', 11100);

INSERT INTO time_slot
VALUES
    (1, 'monday', '08:00:00', '18:00:00'),
    (1, 'tuesday', '08:00:00', '18:00:00'),
    (1, 'wednesday', '08:00:00', '18:00:00'),
    (1, 'thursday', '08:00:00', '18:00:00'),
    (1, 'friday', '08:00:00', '18:00:00'),
    (2, 'monday', '13:00:00', '18:00:00'),
    (2, 'wednesday', '13:00:00', '18:00:00'),
    (2, 'friday', '13:00:00', '18:00:00'),
    (3, 'saturday', '8:00:00', '18:00:00'),
    (3, 'sunday', '8:00:00', '18:00:00');

INSERT INTO customers (first_name,last_name,date_of_birth,email_address,address_line,zip,city)
VALUES
  ('Candice','Cain','1997-08-12 ','praesent.interdum@google.ca','638 Ligula Rd.',10240,'bangkok'),
  ('Wing','Jayme','1942-01-21 ','sed.consequat@google.net','501-177 Metus Av.',10555,'bangkok'),
  ('Ezra','Molly','2000-03-06 ','pede.cras.vulputate@protonmail.com','483-1675 Lorem Av.',80050,'bangkok'),
  ('Adena','Mercedes','1964-11-13 ','lobortis.quis@yahoo.net','Ap #278-4039 Risus Ave',11100,'bangkok'),
  ('Keelie','Beatrice','2003-06-13 ','mattis.semper.dui@hotmail.edu','Ap #624-1234 Nunc Road',10240,'phuket'),
  ('Winifred','Cain','1969-07-13 ','at.velit.pellentesque@outlook.org','738-7453 Odio. Rd.',10555,'phuket'),
  ('Jessica','Keelie','1947-10-01 ','metus.vivamus@outlook.ca','P.O. Box 875, 8686 Nunc Road',80050,'phuket'),
  ('Cara','Clementine','1955-06-30 ','accumsan@hotmail.edu','Ap #857-905 Augue, Rd.',11100,'phuket'),
  ('Ebony','Bo','2003-06-06 ','dignissim.magna@yahoo.couk','P.O. Box 915, 7473 Sem Rd.',10240,'singapore'),
  ('Castor','Giselle','1972-08-25 ','phasellus@protonmail.net','992-3010 Dapibus Av.',10555,'singapore'),
  ('Channing','Shaeleigh','1986-08-16 ','facilisis.non@protonmail.edu','723-1668 Felis Ave',80050,'singapore'),
  ('Benjamin','Chloe','1967-05-31 ','ac@icloud.com','Ap #665-1738 Ante St.',11100,'singapore'),
  ('Tamekah','Zia','2006-08-09 ','quis@aol.edu','573-4325 Vel St.',10240,'pattaya'),
  ('Carson','Paula','1942-09-17 ','dolor.elit@aol.com','323-7900 Est St.',10555,'pattaya'),
  ('Kiara','Honorato','1964-11-23 ','ac@outlook.edu','P.O. Box 475, 3053 Dictum Ave',80050,'pattaya'),
  ('Sasha','Shea','1988-01-09 ','et.magnis@protonmail.edu','1555 Ipsum. Av.',11100,'pattaya'),
  ('Leilani','Sebastian','1999-05-12 ','sollicitudin.commodo@google.net','8242 Venenatis Rd.',10240,'bangkok'),
  ('Zahir','Vaughan','1943-07-07 ','erat@google.couk','Ap #162-9303 Fringilla Road',10555,'bangkok'),
  ('Cody','Carolyn','2008-09-06 ','donec.dignissim@icloud.net','Ap #707-3917 Vivamus Road',80050,'bangkok'),
  ('Martin','Joel','1950-01-09 ','vitae.semper@google.com','P.O. Box 496, 714 Lobortis Street',11100,'bangkok');

INSERT INTO employees (first_name,last_name,date_of_birth,email_address,time_slot_id,address_line,zip,city)
VALUES
  ('Jelani','Mark','1962-01-13 ','scelerisque.sed.sapien@outlook.net',1,'135-9719 Phasellus Road',10240,'bangkok'),
  ('Hilda','Carolyn','1971-10-04 ','ante@outlook.org',2,'8859 Sagittis Avenue',10555,'bangkok'),
  ('Hiram','Shannon','1984-11-21 ','elit.etiam@icloud.edu',3,'662-2710 Donec Rd.',80050,'bangkok'),
  ('Raven','Xyla','1952-04-24 ','ipsum@aol.ca',4,'136-9653 A, Rd.',11100,'bangkok'),
  ('Ezekiel','Knox','1941-02-05 ','adipiscing.lobortis@outlook.net',1,'Ap #708-3722 Scelerisque Road',10240,'phuket'),
  ('Aidan','Roanna','2006-08-24 ','luctus@hotmail.com',2,'Ap #739-2988 Urna Street',10555,'phuket'),
  ('Howard','Justin','1979-03-23 ','at.risus@protonmail.com',3,'5093 Enim Avenue',80050,'phuket'),
  ('Rajah','Quinlan','1977-08-21 ','proin.eget@protonmail.ca',4,'Ap #376-3657 Suspendisse Avenue',11100,'phuket'),
  ('Bethany','Dawn','1994-01-09 ','felis.eget@aol.com',1,'1674 Orci. Rd.',10240,'singapore'),
  ('Irene','Oprah','1946-06-26 ','ipsum.leo@hotmail.com',2,'5047 Facilisis St.',10555,'singapore');

INSERT INTO suppliers (telephone_number,email_address,address_line,zip,city)
VALUES
  ('074-154-6457','fringilla.porttitor@protonmail.ca','9762 Fermentum Road',10555,'bangkok'),
  ('016-229-7593','diam.lorem@yahoo.org','Ap #571-1264 Quam Street',10240,'pattaya'),
  ('004-635-2513','ut@icloud.couk','Ap #725-7284 Nec Av.',11100,'phuket'),
  ('011-591-0672','luctus.sit@aol.com','5075 Tristique St.',80050,'singapore');


INSERT INTO job (job_name, salary)
VALUES
    ('barista', '25000'),
    ('janitor', '18000'),
    ('delivery', '22000'),
    ('marketing', '20000'),
    ('manager', '40000');

INSERT INTO positions(employee_id, job_id)
VALUES
    (1, 5),
    (2, 1),
    (3, 1),
    (4, 1),
    (5, 2),
    (6, 2),
    (7, 3),
    (8, 4),
    (9, 4),
    (10, 3);

INSERT INTO menu(product_name, price_per_unit)
VALUES
    ('espresso', 40),
    ('cappuccino', 60),
    ('latte', 60),
    ('hot chocolate', 60),
    ('iced chocolate', 60),
    ('caramel macchiato', 80);

INSERT INTO stock(stock_name, units)
VALUES
    ('brazilian coffee beans', 40),
    ('local coffee beans', 100),
    ('milk', 100),
    ('water', 200),
    ('cocoa powder', 200),
    ('caramel syrup', 60);

INSERT INTO product(product_id, stock_id)
VALUES
    (1, 1),
    (1, 4),
    (2, 2),
    (2, 3),
    (2, 4),
    (3, 2),
    (3, 3),
    (3, 4),
    (4, 3),
    (4, 5),
    (5, 3),
    (5, 5),
    (6, 2),
    (6, 3),
    (6, 4),
    (6, 6);

INSERT INTO stock_supplier(stock_id, supplier_id)
VALUES
    (1, 4),
    (2, 2),
    (3, 3),
    (5, 3),
    (4, 4),
    (6, 4);
