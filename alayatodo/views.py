from alayatodo import app
from alayatodo.database import db_session
from alayatodo.models import Todo, User
from flask import (
    g,
    redirect,
    render_template,
    request,
    session,
    flash,
    jsonify
    )

@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        #removed .decode('utf-8') on first l to get rid of Attribute Error str
        readme = "".join(l for l in f)
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_POST():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter(User.username == username, User.password ==
                             password).first()
    #sql = "SELECT * FROM users WHERE username = '%s' AND password = '%s'";
    #cur = g.db.execute(sql % (username, password))
    #user = cur.fetchone()
    #print(dict(user))
    if user:
        session['user'] = getUserSessionInfo(user)
        session['logged_in'] = True
        return redirect('/todo')

    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    #cur = g.db.execute("SELECT * FROM todos WHERE id ='%s'" % id)
    #todo = cur.fetchone()
    curr_uid = session['user']['id']
    todo = Todo.query.filter(Todo.user_id == curr_uid, Todo.id ==id).first()
    if todo:
        return render_template('todo.html', todo=todo)
    else:
        return todos()

@app.route('/todo/<id>/json', methods=['GET'])
def todo_json(id):
    curr_uid = session['user']['id']
    todo = Todo.query.filter(Todo.user_id == curr_uid, Todo.id ==id).first()
    if todo:
        return jsonify(todo.serialize)

    else:
        return todos()

@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
def todos():
    if not session.get('logged_in'):
        return redirect('/login')
    #cur = g.db.execute("SELECT * FROM todos")
    #todos = cur.fetchall()
    todos = Todo.query.filter(Todo.user_id ==
                              session['user']['id']).all()
    print(todos)
    return render_template('todos.html', todos=todos)


@app.route('/todo/paginate/<int:p>', methods=['GET'])
def todos_paginate(p):
    if not session.get('logged_in'):
        return redirect('/login')
    #cur = g.db.execute("SELECT * FROM todos")
    #todos = cur.fetchall()
    todos = Todo.query.filter(Todo.user_id ==
                              session['user']['id']).paginate(per_page=3,page=p)
    print(todos)
    return render_template('todos_paginate.html', todos=todos)

@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')
    des = request.form.get('description', '')
    if des != "":
        t = Todo(session['user']['id'],des)
        db_session.add(t)
        db_session.commit()
        flash("Thing added!")
        #g.db.execute(
        #    "INSERT INTO todos (user_id, description) VALUES ('%s', '%s')"
        #    % (session['user']['id'], request.form.get('description', ''))
        #)
        #g.db.commit()
    else:
        flash("Description cannot be empty!", 'error')
    return redirect('/todo')


@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    t = Todo.query.get(id)
    current_db_sessions = db_session.object_session(t)
    current_db_sessions.delete(t)
    current_db_sessions.commit()
    #g.db.execute("DELETE FROM todos WHERE id ='%s'" % id)
    #g.db.caommit()
    flash("Todo Deleted!")
    return redirect('/todo')

def getUserSessionInfo(user):
    return {'id':user.id, 'username': user.username, 'password': user.password}
