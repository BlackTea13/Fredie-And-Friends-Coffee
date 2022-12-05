DROP SCHEMA IF EXISTS faf_coffeeshop;

CREATE SCHEMA faf_coffeeshop;
USE faf_coffeeshop;

DROP TABLE IF EXISTS district_zip;
CREATE TABLE district_zip (
    district varchar(20),
    zip int,
    PRIMARY KEY(zip)
);

DROP TABLE IF EXISTS city_country;
CREATE TABLE city_country(
    city varchar(40),
    country varchar(40),
    PRIMARY KEY (city)
);

DROP TABLE IF EXISTS time_slot;
CREATE TABLE time_slot(
    time_slot_id int,
    work_day char(10),
    start_time time,
    end_time time,
    PRIMARY KEY (time_slot_id, work_day, start_time, end_time)
);

SHOW FULL COLUMNS FROM district_zip;

DROP TABLE IF EXISTS customers;
CREATE TABLE customers (
    customer_id int auto_increment,
    first_name varchar(20) null,
    last_name varchar(20) null,
    date_of_birth date,
    email_address varchar(320),
    address_line varchar(600),
    zip int,
    city varchar(40),
    PRIMARY KEY (customer_id),
    FOREIGN KEY (zip) REFERENCES district_zip(zip),
    FOREIGN KEY (city) REFERENCES city_country(city)
);

DROP TABLE IF EXISTS employees;
CREATE TABLE employees (
    employee_id int auto_increment,
    first_name varchar(20),
    last_name varchar(20),
    date_of_birth date,
    email_address varchar(320),
    time_slot_id int,
    address_line varchar(600),
    zip int,
    city varchar(20),
    PRIMARY KEY (employee_id),
    FOREIGN KEY (zip) REFERENCES district_zip(zip),
    FOREIGN KEY (city) REFERENCES city_country(city)

);

DROP TABLE IF EXISTS suppliers;
CREATE TABLE suppliers(
    supplier_id int auto_increment,
    telephone_number varchar(15),
    email_address varchar(320),
    address_line varchar(600),
    zip int,
    city varchar(20),
    PRIMARY KEY (supplier_id),
    FOREIGN KEY (zip) REFERENCES district_zip(zip),
    FOREIGN KEY (city) REFERENCES city_country(city)
);

DROP TABLE IF EXISTS menu;
CREATE TABLE menu(
    product_id int auto_increment,
    product_name varchar(600),
    price_per_unit float,
    PRIMARY KEY (product_id)

);

DROP TABLE IF EXISTS orders;
CREATE TABLE orders(
    order_id int auto_increment,
    customer_id int,
    order_date date,
    PRIMARY KEY (order_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

DROP TABLE IF EXISTS order_line;
CREATE TABLE order_line(
    order_id int,
    product_id int,
    quantity int,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES menu(product_id)
);

DROP TABLE IF EXISTS stock;
CREATE TABLE stock(
    stock_id int auto_increment,
    stock_name varchar(80),
    units int,
    PRIMARY KEY (stock_id)
);

DROP TABLE IF EXISTS product;
CREATE TABLE product(
    product_id int,
    stock_id int,
    PRIMARY KEY (product_id, stock_id),
    FOREIGN KEY (product_id) REFERENCES menu(product_id),
    FOREIGN KEY (stock_id) REFERENCES stock(stock_id)
);

DROP TABLE IF EXISTS stock_supplier;
CREATE TABLE stock_supplier(
    stock_id int,
    supplier_id int,
    PRIMARY KEY (stock_id, supplier_id),
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);

DROP TABLE IF EXISTS job;
CREATE TABLE job(
    job_id int auto_increment,
    job_name varchar(100),
    salary numeric(15,2),
    PRIMARY KEY (job_id)
);

DROP TABLE IF EXISTS positions;
CREATE TABLE positions(
    employee_id int,
    job_id int,
    PRIMARY KEY (employee_id, job_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
    FOREIGN KEY (job_id) REFERENCES job(job_id)
);

DROP TABLE IF EXISTS users;
create table users
(
    user_id    int auto_increment,
    first_name varchar(30)  null,
    last_name  varchar(30)  null,
    username   varchar(20)  unique,
    email      varchar(30)  null,
    password   varchar(128) null,
    role_id    int          null,
    PRIMARY KEY (user_id)
);




