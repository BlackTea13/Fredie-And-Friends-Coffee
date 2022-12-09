from flask import Flask, render_template, request, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
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
        return render_template('register.html', zip_codes=zip_codes, cities=cities)
    
    elif request.method == 'POST':
        userDetails = request.form
        # Check the password and confirm password
        if userDetails['password'] != userDetails['confirm_password']:
            flash('Passwords do not match', 'danger')
            return render_template('register.html')

        p1 = userDetails['first_name']
        p2 = userDetails['last_name']
        p3 = userDetails['username']
        p4 = userDetails['date_of_birth']
        p5 = userDetails['email']
        p6 = userDetails['address_line']
        p7 = userDetails['zip_code']
        p8 = userDetails['city']
        p9 = userDetails['password']
        

        hashed_pw = generate_password_hash(p9)

        queryStatement_addUser = (
            f"INSERT INTO "
            f"users(first_name,last_name, username, email, password, role_id) "
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


# this function only works with SQL query output
# as the argument
def get_countries_dictionary(input: dict[list]):
    dic = {}
    for item in input:
        city, country = item
        if item[country] not in dic:
            dic[ item[country] ] = [item[city]]
        elif  item[country] in dic:
            dic[ item[country] ] += [item[city]]
    return dic


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        loginForm = request.form
        username = loginForm['username']
        user_data = get_user_data(username)
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
                session['userEmail'] = user['email']
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
    

def get_user_data(username) -> dict:
    return None

@app.route('/profile/<string:username>', methods=['GET'])
def profile(username):
    return render_template('User/profile.html')

@app.route('/profile/<string:username>/edit', methods=['GET', "POST"])
def editProfile(username):
    return render_template('User/editProfile.html')

@app.route('/menu/', methods=['GET'])
def menu():
    return render_template('menu.html')

@app.route('/create-order/', methods=['GET', 'POST'])
def write_blog():
    return render_template('create-order.html')

@app.route('/view-orders/', methods=['GET'])
def view_orders():    
    if 'userroleid' not in session:
        flash('You are not logged in!', 'danger')
        return redirect('/')
    elif 'userroleid' in session:   
        print(session['username'])
        return render_template('Orders/view_orders.html')


# @app.route('/view-my-order/')
# def my_blogs():
#     return render_template('my-orders.html')


# @app.route('/view-orders/')
# def my_blogs():
#     return render_template('view-orders.html')


# @app.route('/view-orders/')
# def my_blogs():
#     return render_template('my-orders.html')


# @app.route('/account/')
# def my_blogs():
#     return render_template('account.html')


# @app.route('/employee/')
# def my_blogs():
#     return render_template('my-orders.html')


# @app.route('/employee/schedule')
# def my_blogs():
#     return render_template('my-orders.html')

# @app.route('/master/')
# def my_blogs():
#     return render_template('master.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out", 'info')
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
