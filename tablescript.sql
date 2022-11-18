CREATE TABLE customers (
    customer_id int auto_increment,
    first_name varchar(20) null,
    last_name varchar(20) null,
    date_of_birth date,
    email_address varchar(320),
    address_line varchar(100),
    district varchar(20),
    city varchar(20),
    PRIMARY KEY (customer_id)
);

CREATE TABLE employees (
    employee_id int auto_increment,
    first_name varchar(20),
    last_name varchar(20),
    date_of_birth date,
    email_address varchar(320),
    PRIMARY KEY (employee_id)
);