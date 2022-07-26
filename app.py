from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Todo %r>' %self.id
@app.route('/', methods=['POST', 'GET'])
#home Page
def index():
    if request.method == 'POST':
        todo_content = request.form['content']
        new_todo = Todo(content=todo_content)
        try:
            db.session.add(new_todo)
            db.session.commit()
            return redirect('/')
        except:
            return "There's an Error while Creating Task!"
    else:
        todos = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', todos=todos)

#deleteTodo
@app.route("/delete/<int:id>")
def delete(id):
    todo_del = Todo.query.get_or_404(id)
    try:
        db.session.delete(todo_del)
        db.session.commit()
        return redirect('/')
    except:
        return "There's an Error in Deleting the Todo"
@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
    todo = Todo.query.get_or_404(id)
    if request.method == 'POST':
        todo.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There's an Error while Updating"
    else:
        return render_template('update.html', todo=todo)


if __name__ == '__main__':
    app.run(debug=True)