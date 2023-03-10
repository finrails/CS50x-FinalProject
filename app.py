from flask import Flask, request, redirect, flash, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask.wrappers import Response
from markupsafe import escape
from datetime import datetime
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/webnance.db"
db.init_app(app)

app.secret_key = "super_secret_key"

with app.app_context():
    try:
        from models import User, Task
    except ImportError as error:
        print(error)

    db.engine.echo = True
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/logout", methods=["POST"])
def destroy_user_session():
    if not session['user_id']:
        flash("You must log in to acess that page.", category="error")
        return redirect(url_for("index"), 400)

    session['user_id'] = None

    flash("You have logged out with success!", category="success")
    return redirect("/")

@app.route("/login/", methods=["GET", "POST"])
def new_user_session():
    if 'user_id' in session:
        if session['user_id']:
            flash("You're already logged in", category="error")
            return redirect('/', 302)

    if request.method == "POST":
        username, raw_password = request.form.get("username"), request.form.get("password")

        user = None

        if not username or not raw_password:
            flash("You must fill all fields...", category="error")
            return render_template("new_user_session.html")

        get_user_query = db.select(User).where(User.username == username)

        user = db.session.execute(get_user_query).scalars().first()

        if not user:
            flash("Invalid username!", category="error")
            return render_template("new_user_session.html")

        
        if check_password_hash(user.hash, raw_password): 
            session['user_id'] = user.id
            flash("You have logged in with success!", category="success")
            return redirect("/")
        else:
            flash("Invalid password or username!", category="error")
            return render_template("new_user_session.html")


    return render_template("new_user_session.html")

@app.route("/tasks/new", methods=["POST"])
def new_task():
    if request.method == "POST":
        task_body = request.form.get("body")
        current_time = datetime.now()

        if "user_id" not in session or not session["user_id"]:
            flash("You must first log in to acess that page", category="error")
            return redirect("/")

        if not task_body:
            flash("You must fill the task with at least one character", category="error")
            return redirect(url_for('show_tasks'))
        
        if len(task_body) > 255:
            flash("The task must not has more than 255 characters", category="error")
            return redirect(url_for('show_tasks'))

        try:
            current_task = Task(user_id=session['user_id'], body=task_body, created_at=current_time, checked="no")
            db.session.add(current_task)
            db.session.commit()
        except:
            flash("Something went wrong.", category="error")
            return redirect(url_for('show_tasks'))

        flash("Task has been created with success", category="success")
        return redirect(url_for('show_tasks'))

@app.route("/tasks/do/<int:task_id>", methods=["POST"])
def complete_task(task_id):
    if request.method == "POST":
        if not 'user_id' in session and not session['user_id']:
            flash("You don't have permission to do this action", category="error")
            redirect(url_for("/"))

        get_task_query = db.select(Task).where(Task.id == task_id)

        try:
            task = db.session.execute(get_task_query).scalars().first()
        except:
            flash("Something went wrong, try again", category="error")
            redirect(url_for("show_tasks"))

        print(f"{task.id} {session['user_id']}")
        if task.user_id != session["user_id"]:
            flash("You don't have permission to do this action", category="error")
            return redirect(url_for("show_tasks"))

        try:
            if task.checked == "no":
                task.checked = "yes"
            else:
                task.checked = "no"
            db.session.add(task)
            db.session.commit()
        except:
            flash("Something went wrong, try again", category="error")
            redirect(url_for("show_tasks"))

        flash("Task has been completed with success", category="success")
        return redirect(url_for("show_tasks"))

@app.route("/tasks/", methods=["GET", "DELETE"])
def show_tasks():
    if 'user_id' in session and session['user_id']:
        get_user_tasks_query = db.select(Task).where(Task.user_id == session['user_id']).order_by(text("created_at desc"))
        tasks = db.session.execute(get_user_tasks_query).scalars()
        return render_template("tasks.html", tasks=tasks)

    flash('You must first log in to acess that page.', category="error")
    return redirect(url_for('index'))

@app.route("/tasks/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    new_content = request.form.get("body")

    if not 'user_id' in session or not session['user_id']:
        flash("You must first log in to acess that content.", category="error")
        return redirect(url_for("show_tasks"))

    if request.method == "POST":
        if not new_content:
            flash("You must fill the content field to edit the task", category="error")
            return redirect(url_for("show_tasks"))

        if not task_id:
            flash("You must input some task to complete this action.", category="error")
            return redirect(url_for('show_tasks'))

        # If there's no task for task_id
        try:
            get_task_query = db.select(Task).where(Task.id == task_id)
            task = db.session.execute(get_task_query).scalars().first()
        except:
            flash("That task doesn't exist", category="error")
            return redirect(url_for("show_tasks"))

        if task.checked == "yes":
            flash("It's impossible to edit a task that already has been completed", category="error")
            return redirect(url_for("show_tasks"))

        if task.user_id != session["user_id"]:
            flash("You don't have permission to do this action", category="error")
            return redirect(url_for("show_tasks"))

        try:
            task.body = new_content
            db.session.add(task)
            db.session.commit()
        except:
            flash("Something went wrong, try again", category="error")
            return redirect(url_for("show_tasks"))

        flash("The task has been edited with success", category="success")
        return redirect(url_for("show_tasks"))

    else:
        return render_template("edit_task.html", task_id=task_id)


@app.route("/tasks/<int:task_id>", methods=["POST", "DELETE"])
def destroy_task(task_id):
    if not task_id:
        flash("You must input some task to complete this action.", category="error")
        return redirect(url_for('show_tasks'))

    if 'user_id' in session and session['user_id']:
        get_task_query = db.select(Task).where(Task.id == task_id)
        
        try:
            task = db.session.execute(get_task_query).scalars().first()
        except:
            flash("This task doesn't exist.", category="error")
            return redirect(url_for('show_tasks'))

        if task.user_id != session['user_id']:
            flash("You don't have the rights to destroy this task.", category="error")
            return redirect(url_for('show_tasks'))

        try:
            db.session.delete(task)
            db.session.commit()
        except:
            flash("Something went really wrong, try it again", category="error")
            return redirect(url_for('show_tasks'))

        flash("The task has been destroyed with success", category="success")
        return redirect(url_for('show_tasks'))

@app.route("/users/new", methods=["GET", "POST"])
def user_new():
    if 'user_id' in session:
        if session['user_id']:
            flash("You're already logged in", category="error")
            return redirect('/', 302)

    if request.method == "POST":
        username, password = request.form.get("username"), request.form.get("password")

        if not username or not password:
            return "You must fill all form fields!", 400

        if len(password) > 72:
            return "The password must be lower than 72 characters!", 400

        if len(username) > 32:
            return "The username must be lower than 32 characters!", 400

        hash_key = generate_password_hash(password)

        current_user = User(username=username, hash=hash_key) 
        db.session.add(current_user)

        try:
            db.session.commit()
            flash("Nice, you've registered a new account.", "success")
            return redirect("/")
        except:
            db.session.flush()
            flash("Something went really wrong!", category="error")
            return redirect(url_for('user_new'))

    else:
        return render_template("new_user.html")




@app.route("/<user_name>")
def show_name(user_name):
    return Response(f"Plain Text with {escape(user_name)}", 200, content_type="text/plain")


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    return render_template("posts.html", post_id=post_id)

@app.route("/projects/")
def show_projects():
    return Response("<h1>Projects</h1>", 200, content_type="text/html")
