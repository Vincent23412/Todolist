from flask import Flask,render_template,request,redirect,session
import json
import pymysql

def load_config(file_path) :
    with open(file_path,"r") as file :
        config = json.load(file)
    return config
db_config = load_config('config.json')['config']

app = Flask(__name__)
app.secret_key='secret'

@app.route('/')
def index() :
    session['log'] = False
    return render_template("login.html")

@app.route('/login',methods=['POST'])
def login() :
    try:
        username = request.form['username']
        password = request.form['password']
        print(username)
        conn = pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
        with conn.cursor() as cur :
            sql = '''SELECT COUNT(*) AS time FROM member WHERE password=%s and username=%s'''
            data = (username,password)
            cur.execute(sql,data)
            if cur.fetchone()['time'] >= 1 :
                session['username'] = username
                session['password'] = password
                session['log'] = True
                return redirect('/member')
            return redirect('/')
    except Exception as e :
        print(e)
        return redirect('/')


@app.route('/register')
def register() :
    return render_template('register.html')


@app.route('/user_register',methods=['POST'])
def user_register() :
    try :
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        conn = pymysql.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cur :
            sql = '''INSERT INTO member(username,password,email) values(%s,%s,%s);'''
            data = (username,password,email)
            cur.execute(sql,data)
            conn.commit()
            return redirect('/')
    except Exception as e :
        print(e)
        return redirect('/register')

@app.route('/member')
def member() :
    log = session.get('log','unknown')
    if log == True :
        return render_template('member.html')
    else:
        redirect('/')

@app.route('/submit_task',methods=['POST'])
def submit():
    try :
        title = request.form['title']
        priority = request.form['priority']
        status = request.form['status']
        start = request.form['start']
        deadline = request.form['deadline']
        description = request.form['description']

        username = session['username']

        conn = pymysql.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cur :
            sql = '''INSERT INTO task(user, title, priority, status, start, deadline, description) VALUES (%s, %s, %s, %s, %s, %s, %s);'''
            data = (username, title, priority, status, start, deadline, description)
            cur.execute(sql,data)
            conn.commit()

        print(title)

    except Exception as e:
        print(e)
    return render_template('member.html')

@app.route('/log_task')
def log_task():
    username = session['username']

    conn = pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    with conn.cursor() as cur :
        sql = '''SELECT title, priority, status, start, deadline, description FROM task WHERE user = %s;'''
        data = (username)
        cur.execute(sql,data)
        result = cur.fetchall()

        print(result)

    return result




if __name__ == '__main__':
    app.run(debug=True)