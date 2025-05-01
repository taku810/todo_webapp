from flask import Flask, render_template, request, redirect, url_for
import json
import os
import threading
import random
import time

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

# タスク自動削除機能
def auto_task_remover():
    """タスクが6つ以上ある場合、ランダムな時間間隔でタスクを1つ削除するバックグラウンドスレッド"""
    while True:
        # ランダムな待機時間（5秒〜15秒）
        wait_time = random.randint(5, 15)
        time.sleep(wait_time)
        
        # タスクのカウントと削除処理
        try:
            todos = get_todos()
            if len(todos) >= 6:
                # ランダムにタスクを1つ選んで削除
                index_to_remove = random.randint(0, len(todos) - 1)
                removed_task = todos.pop(index_to_remove)
                save_todos(todos)
                print(f"自動削除: タスク '{removed_task['task']}' が{wait_time}秒後に削除されました")
        except Exception as e:
            print(f"自動削除エラー: {str(e)}")

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
    # タスク自動削除スレッドを開始（デーモンスレッドとして実行）
    auto_remover_thread = threading.Thread(target=auto_task_remover, daemon=True)
    auto_remover_thread.start()
    print("タスク自動削除機能が有効になりました（タスクが6つ以上の場合にランダムな間隔で削除）")
    
    app.run(debug=True)