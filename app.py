from flask import Flask, render_template, request, session, redirect, jsonify, g
import sqlite3
import pickle


app = Flask(__name__)
app.secret_key = b'random string...'


member_data = {}
message_data = []
member_data_file = 'member_data.dat'
message_data_file = 'message_data.dat'


# load member_data from file.
try:
    with open(member_data_file, "rb") as f:
        list = pickle.load(f)
        if list != None:
            member_data = list
except:
    pass


# load message_data from file.
try:
    with open(message_data_file, "rb") as f:
        list = pickle.load(f)
        if list != None:
            message_data = list
except:
    pass

# get Database Object.
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('sample.sqlite3')
    return g.db


# close Dataabse Object.
def close_db(e=None):
    db = g.pop('db', None)


    if db is not None:
        db.close()


# access top page.
@app.route('/', methods=['GET'])
def index():
    mydata = []
    db = get_db()
    cur = db.execute("select * from mydata")
    mydata = cur.fetchall()
    return render_template('index.html', \
        title='Index', \
        message='※SQLite3 Database',
        alert='This is SQLite3 Database Sample!',
        data=mydata)


# post message.
@app.route('/post', methods=['POST'])
def postMsg():
    global message_data
    id = request.form.get('id')
    msg = request.form.get('comment')
    message_data.append((id, msg))
    if len(message_data) > 25:
        message_data.pop(0)
    try:
        with open(message_data_file, 'wb') as f:
            pickle.dump(message_data, f)
    except:
        pass
    return 'True'




# get messages.
@app.route('/messages', methods=['POST'])
def getMsg():
    global message_data
    return jsonify(message_data)


# login form sended.
@app.route('/login', methods=['POST'])
def login_post():
    global member_data, message_data
    id = request.form.get('id')
    pswd = request.form.get('pass')
    if id in member_data:
        if pswd == member_data[id]:
            flg = 'True'
        else:
            flg = 'False'
    else:
        member_data[id] = pswd
        flg = 'True'
        try:
            with open(member_data_file, 'wb') as f:
                pickle.dump(member_data, f)
        except:
            pass
    return flg
    


if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost')