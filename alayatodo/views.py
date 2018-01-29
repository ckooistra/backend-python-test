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
        readme = "".join(l.decode('utf-8') for l in f)
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
    if user:
        session['user'] = getUserSessionInfo(user)
        session['logged_in'] = True
        return redirect('/todos/1')

    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    curr_uid = session['user']['id']
    todo = Todo.query.filter(Todo.user_id == curr_uid, Todo.id ==id).first()
    return render_template('todo.html', todo=todo)

    #If the url leads to a do owned by the logged in user otherwise switch back
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


#@app.route('/todos', methods=['GET'])
@app.route('/todos/<int:p>', methods=['GET'])
def todos(p):
    if not session.get('logged_in'):
        return redirect('/login')

    #Get list of todos owned by logged in user
    todos = Todo.query.filter(Todo.user_id ==
                              session['user']['id']).paginate(per_page=5,page=p)
    return render_template('todos.html', todos=todos)


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')

    des = request.form.get('description', '')

    t = Todo(session['user']['id'],des, False)
    db_session.add(t)
    db_session.commit()

    return redirect('/todos/1')
@app.route('/complete/<id>', methods=['POST'])
def complete(id):
    t = Todo.query.get(id)
    if t.complete == True:
        t.complete = False
    else:
        t.complete = True
    current_db_sessions = db_session.object_session(t)
    current_db_sessions.merge(t)
    current_db_sessions.commit()

    return redirect('/todos/1')



@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')

    t = Todo.query.get(id)
    current_db_sessions = db_session.object_session(t)
    current_db_sessions.delete(t)
    current_db_sessions.commit()

    return redirect('/todos/1')

def getUserSessionInfo(user):
    return {'id':user.id, 'username': user.username, 'password': user.password}
