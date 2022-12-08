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
        zip_codes_dic = cur.fetchall()
        cur.close()
        print(zip_codes_dic)
        return render_template('register.html', zip_codes=zip_codes_dic)
    elif request.method == 'POST':
        userDetails = request.form
        # Check the password and confirm password
        if userDetails['password'] != userDetails['confirm_password']:
            flash('Passwords do not match', 'danger')
            return render_template('register.html')

        p1 = userDetails['first_name']
        p2 = userDetails['last_name']
        p3 = userDetails['username']
        p4 = userDetails['email']
        p5 = userDetails['address_line']
        p6 = userDetails['zip_code']
        p7 = userDetails['password']
        
        print(p6)
        hashed_pw = generate_password_hash(p7)

        print(p1 + "," + p2 + "," + p3 + "," + p4 + "," + p5)

        queryStatement_addUser = (
            f"INSERT INTO "
            f"users(first_name,last_name, username, email, password, role_id) "
            f"VALUES('{p1}', '{p2}', '{p3}', '{p4}','{hashed_pw}', 1);"
        )
        
        print(check_password_hash(hashed_pw, p5))
        print(queryStatement_addUser)
        cur = mysql.connection.cursor()
        cur.execute(queryStatement_addUser)
        mysql.connection.commit()
        cur.close()

        flash("Form Submitted Successfully.", "success")
        return redirect('/')
    return render_template('register.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        loginForm = request.form
        username = loginForm['username']
        cur = mysql.connection.cursor()
        queryStatement = f"SELECT * FROM users WHERE username = '{username}'"
        numRow = cur.execute(queryStatement)
        if numRow > 0:
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
                #flash("Log In successful", 'success')
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
        queryStatement = f""
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
