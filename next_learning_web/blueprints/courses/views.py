from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from models.course import Course
import peewee as pw
from flask_login import login_user, logout_user, login_required, current_user


courses_blueprint = Blueprint('courses',
                            __name__,
                            template_folder='templates')

@courses_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('courses/new.html')

@courses_blueprint.route('/', methods=['POST'])
def create():
    teacher = User.get_or_none(User.id == current_user.id)
    print(teacher.id)
    title = request.form.get("course_name")
    new_course = Course(title = title, teacher = teacher.id)
    if new_course.save():
        flash("Successfully created the course!","success")

        return redirect(url_for("courses.show"))  
    else:
        flash(new_course.errors, "danger")
        return redirect(url_for("courses.new"))


@courses_blueprint.route('/', methods=['GET'])
def show():
    return render_template("courses/show.html")