from flask import Flask, render_template, request, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
from datetime import datetime
import yaml

app = Flask(__name__)
app.config['SECRET_KEY'] = "Never push this line to github public repo"
cred = yaml.load(open('cred.yaml'), Loader=yaml.Loader)
app.config['MYSQL_HOST'] = cred['mysql_host']
app.config['MYSQL_USER'] = cred['mysql_user']
app.config['MYSQL_PASSWORD'] = cred['mysql_password']
app.config['MYSQL_DB'] = cred['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        queryStatement = (
            f"SELECT zip "
            f"FROM district_zip;"
        )
        cur = mysql.connection.cursor()
        cur.execute(queryStatement)
        zip_codes = cur.fetchall()

        queryStatement = (
            f"SELECT * "
            f"FROM city_country;"
        )
        cur.execute(queryStatement)
        city_country = cur.fetchall()
        cur.close()
        countries_dic = get_countries_dictionary(city_country)
        cities = list(countries_dic.values())
        cities = [city for sublist in cities for city in sublist]
        return render_template('register.html', zip_codes=zip_codes, cities=cities, today=datetime.date(datetime.now()))

    elif request.method == 'POST':
        userDetails = request.form

        if not is_username_unique(userDetails['username']):
            flash("username not unique", "danger")
            return redirect('/register')
        if not is_email_unique(userDetails['email']):
            flash("email is not unique", "danger")
            return redirect('/register')
        # Check the password and confirm password
        if userDetails['password'] != userDetails['confirm_password']:
            flash('Passwords do not match', 'danger')
            return render_template('register.html')

        p9 = userDetails['password']

        hashed_pw = generate_password_hash(p9)

        queryStatement_addUser = (
            f"INSERT INTO "
            f"users(first_name,last_name, username, email_address, password, role_id) "
            f"VALUES('{userDetails['first_name']}',"
            f"'{userDetails['last_name']}', '{userDetails['username']}',"
            f"'{userDetails['email']}','{hashed_pw}', 1);"
        )

        queryStatement_addCustomer = (
            f"INSERT INTO "
            f"customers(first_name,last_name,date_of_birth,email_address,address_line,zip,city) "
            f"VALUES('{userDetails['first_name']}','{userDetails['last_name']}',"
            f"'{userDetails['date_of_birth']}','{userDetails['email']}',"
            f"'{userDetails['address_line']}',{userDetails['zip_code']},"
            f"'{userDetails['city']}');"
        )

        print(queryStatement_addUser)
        print(queryStatement_addCustomer)
        cur = mysql.connection.cursor()
        cur.execute(queryStatement_addUser)
        cur.execute(queryStatement_addCustomer)
        mysql.connection.commit()
        cur.close()

        flash("Form Submitted Successfully.", "success")
        return redirect('/')
    return render_template('register.html')


def is_username_unique(username):
    cur = mysql.connection.cursor()
    queryStatement = (
        f"SELECT username "
        f"FROM users;"
    )
    numRow = cur.execute(queryStatement)
    print(numRow)
    if numRow <= 0:
        return True
    usernames = cur.fetchall()
    cur.close()
    usernames = [u['username'] for u in usernames]
    if username in usernames:
        return False
    return True


def is_email_unique(email):
    tables_to_query = ['users', 'customers', 'employees', 'suppliers']
    
    emails = []
    cur = mysql.connection.cursor()
    for table in tables_to_query:
        queryStatement = (
            f"SELECT email_address "
            f"FROM {table};"
        )
        numRow = cur.execute(queryStatement)
        if numRow <= 0:
            continue
        emails.extend([u['email_address'] for u in cur.fetchall()])
    cur.close()
    if email in emails:
        return False
    return True
        
        
# this function only works with SQL query output
# as the argument
def get_countries_dictionary(input: dict[list]):
    dic = {}
    for item in input:
        city, country = item
        if item[country] not in dic:
            dic[item[country]] = [item[city]]
        elif item[country] in dic:
            dic[item[country]] += [item[city]]
    return dic


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        loginForm = request.form
        username = loginForm['username']
        cur = mysql.connection.cursor()
        queryStatement_user = f"SELECT * FROM users WHERE username = '{username}'"
        numRow_user = cur.execute(queryStatement_user)

        if numRow_user > 0:
            user = cur.fetchone()
            if check_password_hash(user['password'], loginForm['password']):
                # Record session information
                session['login'] = True
                session['username'] = user['username']
                session['userroleid'] = str(user['role_id'])
                session['firstName'] = user['first_name']
                session['lastName'] = user['last_name']
                session['userEmail'] = user['email_address']
                print(session['username'] +
                      " roleid: " + session['userroleid'])
                flash('Welcome ' + session['firstName'], 'success')
                return redirect('/')
            else:
                cur.close()
                flash("Password doesn't not match", 'danger')
        else:
            cur.close()
            flash('User not found', 'danger')
            return render_template('login.html')
        cur.close()
        return redirect('/')
    return render_template('login.html')


def get_employee_info(email):
    cur = mysql.connection.cursor()
    queryStatement = (
        f"SELECT j.job_name, j.salary "
        f"FROM users as u "
        f"JOIN employees as e on u.email_address = e.email_address "
        f"JOIN positions as p on e.employee_id = p.employee_id "
        f"Join job as j on p.job_id = j.job_id "
        f"WHERE u.email_address = '{session['userEmail']}';"
    )
    cur.execute(queryStatement)
    employee = cur.fetchone()
    cur.close()
    return employee

@app.route('/profile/employee/<string:username>', methods=['GET'])
def profile(username):
    if 'login' not in session:
        flash('you are not logged in!', 'danger')
        return redirect('/')
    if session['userroleid'] == 2:
        jobInfo = get_employee_info(session['userEmail'])
        return render_template('Employee/employeeProfile.html', jobInfo=jobInfo)
    return render_template('User/profile.html')

@app.route('/profile/<string:username>', methods=['GET'])
def profile2(username):
    if 'login' not in session:
        flash('you are not logged in!', 'danger')
        return redirect('/')
    jobInfo = get_employee_info(session['userEmail'])
    return render_template('Employee/employeeProfile.html', jobInfo=jobInfo)

@app.route('/profile/<string:username>/edit', methods=['GET', "POST"])
def editProfile(username):
    # if (session['login'] != None and session['login']):
    #     return render_template('User/editProfile.html')
    if request.method == 'GET':
        if 'login' not in session:
            flash('you are not logged in!', 'danger')
            return redirect('/')
        queryStatement = (
            f"SELECT zip "
            f"FROM district_zip;"
        )
        cur = mysql.connection.cursor()
        cur.execute(queryStatement)
        zip_codes = cur.fetchall()

        queryStatement = (
            f"SELECT * "
            f"FROM city_country;"
        )
        cur.execute(queryStatement)
        city_country = cur.fetchall()

        queryStatement = (
            f"SELECT address_line "
            f"FROM customers "
            f"WHERE email_address = '{session['userEmail']}'; "
        )
        cur.execute(queryStatement)
        address_line = cur.fetchall()
        print(address_line[0])
        print(type(address_line[0]))
        print(address_line[0].get('address_line'))
        cur.close()
        countries_dic = get_countries_dictionary(city_country)
        cities = list(countries_dic.values())
        cities = [city for sublist in cities for city in sublist]
        return render_template('User/editProfile.html', zip_codes=zip_codes, cities=cities, today=datetime.date(datetime.now()), address_line=address_line[0].get('address_line'))

    elif request.method == 'POST':
        if 'login' not in session:
            flash('you are not logged in!', 'danger')
            return redirect('/')
        userDetails = request.form    
        # edit user
        queryStatement_editUser = (
            f"UPDATE users "
            f"SET first_name = '{userDetails['first_name']}', "
            f"last_name = '{userDetails['last_name']}', "
            f"username = '{userDetails['username']}', "
            f"email_address = '{userDetails['email_address']}' "
            f"WHERE email_address = '{session['userEmail']}'; "
        )
        # address_line
        queryStatement_editCustomer = (
            f"UPDATE customers "
            f"SET first_name = '{userDetails['first_name']}', "
            f"last_name = '{userDetails['last_name']}', "
            f"email_address = '{userDetails['email_address']}', "
            f"address_line = '{userDetails['address_line']}', "
            f"zip = '{userDetails['zip_code']}', "
            f"city = '{userDetails['city']}' "
            f"WHERE email_address = '{session['userEmail']}'; "   
        )
        cur = mysql.connection.cursor()
        cur.execute(queryStatement_editUser)
        cur.execute(queryStatement_editCustomer)
        mysql.connection.commit()
        cur.close()
        # might have to change the session var
        session['username'] = userDetails['username']
        session['firstName'] = userDetails['first_name']
        session['lastName'] = userDetails['last_name']
        session['userEmail'] = userDetails['email_address']
            

        flash("Form Submitted Successfully.", "success")
        return redirect('/')


    return render_template('User/editProfile.html')


@app.route('/profile/<string:username>/change', methods=['GET', "POST"])
def changePass(username):
    if request.method == 'POST':
        if 'login' not in session:
            flash('you are not logged in!', 'danger')
            return redirect('/')
        userDetails = request.form
        # Check the password and confirm password
        if userDetails['password'] != userDetails['confirm_password']:
            flash('Passwords do not match', 'danger')
            return render_template('User/changePass.html')
        p9 = userDetails['password']
        hashed_pw = generate_password_hash(p9)
        queryStatement_changePass = (
            f"UPDATE users "
            f"SET password = '{hashed_pw}' "
            f"WHERE email_address = '{session['userEmail']}'; "
        )
        cur = mysql.connection.cursor()
        cur.execute(queryStatement_changePass)
        mysql.connection.commit()
        cur.close()

        flash("Form Submitted Successfully.", "success")
        return redirect('/')
    return render_template('User/changePass.html')

@app.route('/employee/<string:name>', methods=['GET'])
def timeslot(name):
    if 'login' not in session:
        flash('you are not logged in!', 'danger')
        return redirect('/')
    time_slot_data = get_time_slot()
    return render_template('/Employee/timeslotPage.html', time_slot_data=time_slot_data)

@app.route('/owner/timeslots', methods=['GET'])
def all_timeslots():
    if 'login' not in session:
        flash('you are not logged in!', 'danger')
        return redirect('/')
    time_slot_data = get_all_time_slot()
    return render_template('/OwnerPage/ownerTimeslotPage.html', time_slot_data=time_slot_data)

def get_all_time_slot():
    cur = mysql.connection.cursor()
    queryStatement = (
        f"SELECT work_day, start_time, end_time, first_name, last_name "
        f"FROM employees join time_slot ts on employees.time_slot_id = ts.time_slot_id "
        f"ORDER BY CASE "
        f"WHEN work_day = 'Monday' THEN 1 "
        f"WHEN work_day = 'Tuesday' THEN 2 "
        f"WHEN work_day = 'Wednesday' THEN 3 "
        f"WHEN work_day = 'Thursday' THEN 4 "
        f"WHEN work_day = 'Friday' THEN 5 "
        f"WHEN work_day = 'Saturday' THEN 6 "
        f"WHEN work_day = 'Sunday' THEN 7 "
        f"END, start_time ASC; ")
    cur.execute(queryStatement)
    allTimeslot = cur.fetchall()
    cur.close()
    return allTimeslot
def get_time_slot():
    cur = mysql.connection.cursor()
    queryStatement = (
    f"SELECT first_name, last_name, work_day, start_time, end_time "
    f"FROM employees join time_slot ts on employees.time_slot_id = ts.time_slot_id "
    f"WHERE email_address = '{session['userEmail'] }'; ")
    cur.execute(queryStatement)
    timeslot = cur.fetchall()
    cur.close()
    return timeslot
    
@app.route('/menu/', methods=['GET', 'POST'])
def menu():
    if request.method == 'GET':
        menu = getAllMenu()
        return render_template('menu.html', menu=menu)
    elif request.method == 'POST':
        if 'login' not in session:
            flash('you are not logged in!', 'danger')
            return redirect('/menu')
        elif session['userroleid'] == '2' or session['userroleid'] == '3':
            flash('you are not a customer! LEAVE.', 'danger')
            return redirect('/menu')
        
        form = request.form
        menu = getAllMenu()
        quantities = {}
        for item in menu:
            itemid = item['product_id']
            itemname = item['product_name']
            if form[itemname] != '' and form[itemname] != '0':
                quantities[itemid] = form[itemname]
        if len(quantities.keys()) == 0:
            flash('nothing in your order!', 'danger')
            return redirect('/menu/')
        print(quantities)
        
        customer_Id = get_customer_Id(session['userEmail'])
        cur = mysql.connection.cursor()
        queryStatement_orders = (
            f"INSERT INTO orders(customer_id, order_date, order_status) "
            f"VALUES ('{customer_Id}', '{datetime.date(datetime.now())}', 'incomplete');"
        )
        cur.execute(queryStatement_orders)
        mysql.connection.commit()
        cur.close()
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT max(order_id) as id FROM orders;")
        order_id = cur.fetchone()['id']
        print(f'LAST ID: {order_id}')
        order_lines = order_line_gen(order_id, quantities)
        cur.execute(order_lines)
        mysql.connection.commit()
        cur.close()
        flash('order placed!')
        return redirect('/view-orders')
        
        
def order_line_gen(order_id, quantities): 
    query = "INSERT INTO order_line VALUES "
    for item in quantities:
        query += f'({order_id}, {item}, {quantities[item]}),'
    query = query[:-1]
    query += ';'
    print(query)
    return query
        

def get_customer_Id(email):
    cur = mysql.connection.cursor()
    cur.execute(f'SELECT customer_id FROM customers WHERE email_address = "{email}"')
    output = cur.fetchone()
    cur.close()
    return output['customer_id']
    

def getAllMenu():
    cur = mysql.connection.cursor()
    queryStatement = (
    f"SELECT product_id, product_name, price_per_unit "
    f"FROM menu; ")
    cur.execute(queryStatement)
    menu = cur.fetchall()
    cur.close()
    return menu


@app.route('/view-orders/', methods=['GET', 'POST'])
def view_orders():
    if request.method == 'GET':
        if 'userroleid' not in session:
            flash('You are not logged in!', 'danger')
            return redirect('/')
        elif session['userroleid'] == '3' or session['userroleid'] == '2':
            orders = orders_by_order_id(get_all_orders())
            cost_for_each_order(orders)
            return render_template('Orders/view_orders_owner.html', orders=orders)
        elif session['userroleid'] == '1':
            orders = orders_by_order_id(get_customer_order(session['userEmail']))
            cost_for_each_order(orders)
            return render_template('Orders/view_orders_customer.html', orders=orders)
    elif request.method == 'POST':
        if 'login' not in session:
            flash('you are not logged in!', 'danger')
            return redirect('/')
        order_id_completed = request.form['order']
        queryStatement = (
            f"UPDATE orders "
            f"SET order_status = 'complete' "
            f"WHERE order_id = %s;"
        )
        cur = mysql.connection.cursor()
        cur.execute(queryStatement, (order_id_completed,))
        mysql.connection.commit()
        cur.close()
        if 'userroleid' not in session:
            flash('You are not logged in!', 'danger')
            return redirect('/')
    return redirect('/view-orders')


def get_all_orders():
    cur = mysql.connection.cursor()
    queryStatement = (
        f"SELECT ol.order_id, first_name, last_name, order_date, order_status, product_name, quantity, price_per_unit "
        f"FROM orders join customers c on c.customer_id = orders.customer_id "
        f"join order_line ol on orders.order_id = ol.order_id "
        f"join menu m on ol.product_id = m.product_id "
        f"ORDER BY order_id DESC;")
    cur.execute(queryStatement)
    all_orders = cur.fetchall()
    cur.close()
    return all_orders


# this function will process SQL Query output into
# dictionary by order_id
def orders_by_order_id(rows):
    orders = {}
    for row in rows:
        if row['order_id'] in orders:
            orders[row['order_id']] += [row]
        elif row['order_id'] not in orders:
            orders[row['order_id']] = [row]
    return orders


def cost_for_each_order(dict):
    for order_id in dict:
        cost = 0
        for item in dict[order_id]:
            cost += item['price_per_unit'] * item['quantity']
        item['total_cost'] = cost


def get_customer_order(email):
    cur = mysql.connection.cursor()
    queryStatement = (
        f"SELECT ol.order_id, first_name, last_name, order_date, order_status, product_name, quantity, price_per_unit "
        f"FROM orders join customers c on c.customer_id = orders.customer_id "
        f"join order_line ol on orders.order_id = ol.order_id "
        f"join menu m on ol.product_id = m.product_id "
        f"WHERE email_address = '{email}' "
        f"ORDER BY order_id DESC;")
    cur.execute(queryStatement)
    customer_orders = cur.fetchall()
    cur.close()
    return customer_orders

# admin page for users
@app.route('/owner', methods=['GET', 'POST'])
def owner():
    if request.method == 'GET':
        queryStatement = (
            f"SELECT username, first_name, last_name, email_address, role_description "
            f"FROM users join roles r on users.role_id = r.role_id "
            f"WHERE role_description != 'Owner'; "
        )
        cur = mysql.connection.cursor()
        cur.execute(queryStatement)
        users_table = cur.fetchall()
        return render_template('OwnerPage/ownerHomePage.html', users_table=users_table)
    # delete user
    elif request.method == 'POST' and request.form['delete'] != None:
        userDetails = request.form
        cur = mysql.connection.cursor()
        queryStatement_userEmail = (
            f"SELECT email_address "
            f"FROM users "
            f"WHERE username= '{userDetails['delete']}'; "
        )
        cur.execute(queryStatement_userEmail)
        userEmail = cur.fetchone()
        email = userEmail['email_address']
        cur.close()
        cur = mysql.connection.cursor()
        queryStatement_deleteUser = (
            f"DELETE FROM users "
            f"WHERE email_address= '{email}' "
        )
        queryStatement_deleteCustomer = (
            f"DELETE FROM customers "
            f"WHERE email_address= '{email}' "
        )
        queryStatement_deleteEmployees = (
            f"DELETE FROM employees "
            f"WHERE email_address= '{email}' "
        )
        cur.execute(queryStatement_deleteUser)
        cur.execute(queryStatement_deleteCustomer)
        cur.execute(queryStatement_deleteEmployees)
        mysql.connection.commit()
        cur.close()

        flash("Delete Successfully.", "success")
        return redirect('/owner')

    return render_template('OwnerPage/ownerHomePage.html')



@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out", 'info')
    return redirect('/')

@app.route('/stock/', methods=['GET'])
def stock():
    if 'login' not in session:
        flash('you are not logged in!', 'danger')
        return redirect('/')
    if session['userroleid'] == '2' or session['userroleid'] == '3':
        stock = get_stock()
        return render_template('Stock/stock.html', stock=stock)
    flash("You don't work here!", 'danger')
    return redirect('/')

def get_stock():
    cur = mysql.connection.cursor()
    queryStatement = (
        f"SELECT * FROM stock;")
    cur.execute(queryStatement)
    current_stock = cur.fetchall()
    cur.close()
    return current_stock

if __name__ == '__main__':
    app.run(debug=True)
