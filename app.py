from flask import Flask, render_template, request, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)
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

# @app.route('/about/')
# def about():
#     return render_template('about.html')

# @app.route('/register/', methods=['GET', 'POST'])
# def register():
#     return render_template('register.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        loginForm = request.form
        username = loginForm['username']
        cur = mysql.connection.cursor()
        queryStatement = f"SELECT * FROM user WHERE username = '{username}'"
        numRow = cur.execute(queryStatement)
        if numRow > 0:
            user =  cur.fetchone()
            if check_password_hash(user['password'], loginForm['password']):

                # Record session information
                session['login'] = True
                session['username'] = user['username']
                session['userroleid'] = str(user['role_id'])
                session['firstName'] = user['first_name']
                session['lastName'] = user['last_name']
                print(session['username'] + " roleid: " + session['userroleid'])
                flash('Welcome ' + session['firstName'], 'success')
                #flash("Log In successful",'success')
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

# @app.route('/logout')
# def logout():
#     return render_template('logout.html')

# @app.route('/orders', methods=['GET', 'POST'])
# def logout():
#     return render_template('logout.html')

# @app.route('/orders/<int:id>',  methods=['GET', 'POST'])
# def logout():
#     return render_template('logout.html')

if __name__ == '__main__':
    app.run(debug=True)