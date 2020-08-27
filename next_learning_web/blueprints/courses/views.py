from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from models.course import Course
from models.student_course import StudentCourse
from models.assignment import Assignment
import peewee as pw
import re
from flask_login import login_user, logout_user, login_required, current_user
from next_learning_web.util.helpers import upload_file_to_s3
from werkzeug import secure_filename


courses_blueprint = Blueprint('courses',
                            __name__,
                            template_folder='templates')

@courses_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('courses/new.html')

@courses_blueprint.route('/', methods=['POST'])
def create():
    params = request.form

    new_course = Course(title=params.get("course_title"), teacher_id=current_user.id)

    if new_course.save():
        flash("Successfully Created a Course!","success")
        return redirect(url_for("users.show", username=current_user.username))  # then redirect to profile page
    else:
        flash(new_course.errors, "danger")
        return redirect(url_for("courses.new"))

@courses_blueprint.route('/<course_title>', methods=['GET'])
def show(course_title):
    students = []

    for info in StudentCourse.select().join(Course).where(Course.title == course_title):
        for student in User.select().where(User.id == info.student_id):
            students.append(student)

    return render_template('courses/show.html', course_title=course_title, students=students)

@courses_blueprint.route('/register', methods=['GET'])
def register():
    courses = []

    for course in Course.select().where(Course.teacher_id == current_user.id):
        print(course)
        courses.append(course)
    
    return render_template('courses/register.html', courses=courses)

@courses_blueprint.route('/enroll', methods=['POST'])
def enroll():
    params = request.form

    username = params.get("username")
    course = params.get("course")

    student = User.get_or_none(User.username == username)
    course = Course.get_or_none(Course.id == course)
    print(student)
    print(course)

    if student and course:
        new_student_course = StudentCourse(student_id=student.id, course_name_id=course.id)

        new_student_course.save()
        flash("Successfully enrolled a student!", "success")
        return redirect(url_for("users.show", username=current_user.username))
    else:
        flash("Failed to enroll student!", "danger")
        return redirect(url_for("courses.register"))
    
