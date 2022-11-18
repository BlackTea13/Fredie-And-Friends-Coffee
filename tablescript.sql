CREATE TABLE customers (
    customer_id int auto_increment primary key, 
    first_name varchar(20) null
    last_name varchar(20) null
    date_of_birth() date,
    address_line varchar(100),
    district varchar(20),
    city varchar(20)
)