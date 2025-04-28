from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# JSONファイルのパスを定義
TODO_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'todos.json')

# JSONファイルが存在しない場合は作成する
def initialize_todos():
    if not os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'w') as f:
            json.dump([], f)

# ToDoリストを取得する関数
def get_todos():
    initialize_todos()
    with open(TODO_FILE, 'r') as f:
        return json.load(f)

# ToDoリストを保存する関数
def save_todos(todos):
    with open(TODO_FILE, 'w') as f:
        json.dump(todos, f)

@app.route('/')
def index():
    todos = get_todos()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    if task:
        todos = get_todos()
        todos.append({"task": task, "completed": False})
        save_todos(todos)
    return redirect(url_for('index'))

@app.route('/delete/<int:index>')
def delete(index):
    todos = get_todos()
    if 0 <= index < len(todos):
        todos.pop(index)
        save_todos(todos)
    return redirect(url_for('index'))

@app.route('/toggle/<int:index>')
def toggle(index):
    todos = get_todos()
    if 0 <= index < len(todos):
        todos[index]['completed'] = not todos[index]['completed']
        save_todos(todos)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)