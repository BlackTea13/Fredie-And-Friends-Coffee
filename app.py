from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/orders', methods=['GET', 'POST'])
def logout():
    return render_template('logout.html')

@app.route('/orders/<int:id>',  methods=['GET', 'POST'])
def logout():
    return render_template('logout.html')

if __name__ == '__main__':
    app.run(debug=True)