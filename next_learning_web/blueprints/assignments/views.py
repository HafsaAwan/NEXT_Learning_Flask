from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from models.course import Course
from models.post import Post
from models.thread import Thread
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

@assignments_blueprint.route('/<course_title>/<user_id>/<post_id>/upload', methods=['POST'])
def upload(user_id, course_title, post_id):
    user = User.get_or_none(User.id == user_id)
    course = Course.get_or_none(Course.title == course_title)
    thread = Thread.get_or_none(Thread.course_id == course.id)

    post =  Post.get_or_none(Post.file_path != 'NULL', Post.thread_id == thread.id)
    
    params = request.form

    title = params.get("title")

    info = StudentCourse.get_or_none(StudentCourse.student_id == user_id, StudentCourse.course_name_id == course.id)
    
    if info:
        if current_user.id == user.id:
            # We check the request.files object for a user_file key. (user_file is the name of the file input on our form). If it's not there, we return an error message.
            if "assignment" not in request.files:
                flash("No file provided!", "danger")
                return redirect(url_for('posts.show', course_name=course_title, user_id=current_user.id, post_id = post.id))
            
            # If the key is in the object, we save it in a variable called file.
            file = request.files["assignment"]

            # we sanitize the filename using the secure_filename helper function provided by the werkzeurg.security module.
            file.filename = secure_filename(file.filename)

            # get path to image on S3 bucket using function in helper.py
            file_path = upload_file_to_s3(file, user.username)
            
            new_assignment = Assignment(title=title, info_id=info.id, file_path=file_path, post_id=post.id)
            
            if new_assignment.save():
                flash("Successfully uploaded!","success")
                return redirect(url_for('posts.show', course_name=course_title, user_id=current_user.id, post_id = post.id))  # then redirect to profile page
            else:
                flash("Upload failed. Please try again!", "danger")
                return redirect(url_for('posts.show', course_name=course_title, user_id=current_user.id, post_id = post.id))
        else:
            flash("Cannot upload assignments for other users", "danger")
            return redirect(url_for('posts.show', course_name=course_title, user_id=current_user.id, post_id = post.id))
            
    else:
        flash("Failed to upload!", "danger")
        return redirect(url_for('posts.show', course_name=course_title, user_id=current_user.id, post_id = post.id))


@assignments_blueprint.route('/<course_title>/<user_id>/<post_id>/submissions', methods=['POST'])
def check(course_title, user_id, post_id):
    current_course = Course.get_or_none(Course.title == course_title)
    current_info = StudentCourse.get_or_none(StudentCourse.course_name_id == current_course.id)
    current_assignment = Assignment.get_or_none(Assignment.post_id == post_id, Assignment.info_id == current_info.id)

    params = request.form

    current_assignment.title = current_assignment.title
    current_assignment.info_id = current_assignment.info_id
    current_assignment.file_path = current_assignment.file_path
    current_assignment.post_id = current_assignment.post_id

    current_assignment.grade_id = params.get('grade')

    if current_assignment.save():
        flash("Successfully graded the student!")
        return redirect(url_for('posts.show', course_name=course_title, user_id=current_user.id, post_id = post_id))
    else:
        flash("Failed to grade the student!")
        return redirect(url_for('posts.show', course_name=course_title, user_id=current_user.id, post_id = post_id))
    