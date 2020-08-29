from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from models.course import Course
from models.student_course import StudentCourse
from models.assignment import Assignment
from models.thread import Thread
from models.post import Post
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
    pass

@courses_blueprint.route('/', methods=['POST'])
def create():
    params = request.form

    new_course = Course(title=params.get("course_title"), teacher_id=current_user.id)

    if new_course.save():
        print("new_course.id",new_course.id)
        new_thread = Thread(course = new_course.id)
        new_thread.save()
        print("new thread", new_thread.id)
        flash("Successfully Created a Course!","success")
        return redirect(url_for("users.show", username=current_user.username))  # then redirect to profile page
    else:
        flash(new_course.errors, "danger")
        return redirect(url_for("users.show"))

@courses_blueprint.route('/<course_title>', methods=['GET'])
def show(course_title):
    current_course = Course.get_or_none(Course.title == course_title)
    students = []

    for info in StudentCourse.select().join(Course).where(Course.title == course_title):
        for student in User.select().where(User.id == info.student_id):
            students.append(student)

    for thread in current_course.thread:
        course_thread = thread
    
    course_posts = []

    for post in Post.select().where(Post.thread_id == course_thread):
        course_posts.append(post)

    course_posts.reverse()
    
    return render_template('courses/show.html', course_title=course_title,students=students, course_posts=course_posts)


@courses_blueprint.route('/<course_title>/enroll', methods=['POST'])
def enroll(course_title):
    params = request.form

    username = params.get("username")

    current_course = Course.get_or_none(Course.title == course_title)
    student = User.get_or_none(User.username == username)
    check_student = StudentCourse.get_or_none(StudentCourse.student_id==student.id, StudentCourse.course_name_id==current_course.id)

    if not check_student:
        if student:
            new_student_course = StudentCourse(student_id=student.id, course_name_id=current_course.id)

            new_student_course.save()
            flash("Successfully enrolled a student!", "success")
            return redirect(url_for("courses.show", course_title=course_title))
        else:
            flash("Failed to enroll student!", "danger")
            return redirect(url_for("courses.show", course_title=course_title))
    else:
        flash("The student is already enrolled in this course!", "danger")
        return redirect(url_for("courses.show", course_title=course_title))
    
