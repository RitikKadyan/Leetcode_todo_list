from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class TodoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    completed = db.Column(db.Boolean)


db.create_all()


@app.route('/')
def index():  # put application's code here
    todo_list = db.session.query(TodoItem).all()
    return render_template("base.html", todo_list=todo_list)


@app.post("/add")
def add():
    name = request.form.get("title")
    new_todo_item = TodoItem(name=name, completed=False)
    db.session.add(new_todo_item)
    db.session.commit()
    return redirect(url_for("index"))


@app.get("/update/<int:todo_id>")
def update(todo_id):
    todo_item = db.session.query(TodoItem).filter(TodoItem.id == todo_id).first()
    todo_item.completed = not todo_item.completed
    db.session.commit()
    return redirect(url_for("index"))


@app.get("/delete/<int:todo_id>")
def delete(todo_id):
    todo_item = db.session.query(TodoItem).filter(TodoItem.id == todo_id).first()
    db.session.delete(todo_item)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run()
