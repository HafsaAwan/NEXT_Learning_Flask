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


assignments_blueprint = Blueprint('assignments',
                            __name__,
                            template_folder='templates')

@assignments_blueprint.route('/<course_id>/new', methods=['GET'])
def new():
    pass

@assignments_blueprint.route('/', methods=['POST'])
def create():
    pass

@assignments_blueprint.route('/<course_id>/<id>/upload', methods=['POST'])
def upload(id, course_id):
    user = User.get_or_none(User.id == id)

    params = request.form

    title = params.get("title")

    info = StudentCourse.get_or_none(StudentCourse.student_id == id, StudentCourse.course_name_id == course_id)
    
    if info:
        if current_user.id == int(id):
            # We check the request.files object for a user_file key. (user_file is the name of the file input on our form). If it's not there, we return an error message.
            if "assignment" not in request.files:
                flash("No file provided!", "danger")
                return redirect(url_for('assignments.new'))
            
            # If the key is in the object, we save it in a variable called file.
            file = request.files["assignment"]

            # we sanitize the filename using the secure_filename helper function provided by the werkzeurg.security module.
            file.filename = secure_filename(file.filename)

            # get path to image on S3 bucket using function in helper.py
            file_path = upload_file_to_s3(file, user.username)
            # print(file_path)
            
            new_assignment = Assignment(title=title, info_id=info.id, file_path=file_path)
            
            if new_assignment.save():
                flash("Successfully uploaded!","success")
                return redirect(url_for("users.show", username=user.username))  # then redirect to profile page
            else:
                flash("Upload failed. Please try again!", "danger")
                return redirect(url_for('assignments.new'))
        else:
            flash("Cannot upload assignments for other users", "danger")
            return redirect(url_for('users.show', username = user.username))
            
    else:
        flash("Failed to upload!", "danger")
        return redirect(url_for('home'))

@assignments_blueprint.route('/<course_title>/submissions', methods=['GET'])
def box(course_title):
    course = Course.get_or_none(Course.title == course_title)


    info = StudentCourse.get_or_none(StudentCourse.student_id == current_user.id, StudentCourse.course_name_id == course.id)

    assignments = []

    for assignment in Assignment.select().where(Assignment.info_id == info.id):
        assignments.append(assignment)

    return render_template('assignments/box.html', assignments=assignments, course=course)