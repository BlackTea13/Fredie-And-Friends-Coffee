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
    work_day char(10) NOT NULL,
    start_time time NOT NULL,
    end_time time NOT NULL,
    PRIMARY KEY (time_slot_id, work_day, start_time, end_time)
);

DROP TABLE IF EXISTS customers;
CREATE TABLE customers (
    customer_id int auto_increment,
    first_name varchar(20) NOT NULL,
    last_name varchar(20) NOT NULL,
    date_of_birth date,
    email_address varchar(320) NOT NULL UNIQUE,
    address_line varchar(600) NOT NULL,
    zip int NOT NULL,
    city varchar(40),
    PRIMARY KEY (customer_id),
    FOREIGN KEY (zip) REFERENCES district_zip(zip),
    FOREIGN KEY (city) REFERENCES city_country(city)
);

DROP TABLE IF EXISTS employees;
CREATE TABLE employees (
    employee_id int auto_increment,
    first_name varchar(20) NOT NULL,
    last_name varchar(20) NOT NULL,
    date_of_birth date,
    email_address varchar(320) NOT NULL UNIQUE,
    time_slot_id int NOT NULL,
    address_line varchar(600) NOT NULL,
    zip int NOT NULL,
    city varchar(20),
    PRIMARY KEY (employee_id),
    FOREIGN KEY (zip) REFERENCES district_zip(zip),
    FOREIGN KEY (city) REFERENCES city_country(city)

);

DROP TABLE IF EXISTS suppliers;
CREATE TABLE suppliers(
    supplier_id int auto_increment,
    telephone_number varchar(15) NOT NULL UNIQUE,
    email_address varchar(320) NOT NULL UNIQUE,
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
    product_name varchar(600) NOT NULL,
    price_per_unit float NOT NULl,
    PRIMARY KEY (product_id)

);

DROP TABLE IF EXISTS orders;
CREATE TABLE orders(
    order_id int auto_increment,
    customer_id int,
    order_date date NOT NULL,
    order_status varchar(20) NOT NULL ENUM('complete', 'incomplete', 'cancelled')
    PRIMARY KEY (order_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

DROP TABLE IF EXISTS order_line;
CREATE TABLE order_line(
    order_id int,
    product_id int,
    quantity int NOT NULL,
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
    salary numeric(15,2) NOT NULL,
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

DROP TABLE IF EXISTS roles;
CREATE TABLE roles
(
    role_id int,
    role_description varchar(30) NOT NULL,
    PRIMARY KEY (role_id)
);

DROP TABLE IF EXISTS users;
CREATE TABLE users
(
    user_id    int auto_increment,
    first_name varchar(30),
    last_name  varchar(30),
    username   varchar(20)  NOT NULL UNIQUE,
    email_address      varchar(300)  NOT NULL UNIQUE,
    password   varchar(128) NOT NULL,
    role_id    int          NOT NULL,
    PRIMARY KEY (user_id),
    FOREIGN KEY (role_id) REFERENCES roles(role_id)
);
