from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from models.course import Course
from models.student_course import StudentCourse
from models.thread import Thread
from models.post import Post
from models.assignment import Assignment
from models.grade import Grade
from models.comment import Comment
import peewee as pw
import re
from flask_login import login_user, logout_user, login_required, current_user
from next_learning_web.util.helpers import upload_file_to_s3
# from werkzeug import secure_filename
from models.post import Post

posts_blueprint = Blueprint('posts',
                            __name__,
                            template_folder='templates')

  

@posts_blueprint.route('/<course_name>/<user_id>/<post_id>', methods=['POST'])
def create(course_name,user_id,post_id):
    # print("inside posts create func  :",course_name)
    user = User.get_or_none(User.id == user_id)
    current_course = Course.get_or_none(Course.title == course_name)
    # print("current_course    ",current_course)
    
    for thread in current_course.thread:
        course_thread = thread
    # print("current_course thread   ",course_thread)
    
    if request.form.get("comment"):
        new_comment = Comment(content=request.form.get("comment"), post=post_id, user=user)
        new_comment.save()
    else:
        if "assignment" in request.files:
            file = request.files["assignment"]
            # file.filename = secure_filename(file.filename)
            file_path = upload_file_to_s3(file, user.username)

            content = request.form.get("post_content")
            new_post = Post(post_content=content, thread=course_thread,user=user, file_path=file_path)
            new_post.save()
        else:
            content = request.form.get("post_content")
            new_post = Post(post_content=content, thread=course_thread,user=user)
            new_post.save()

    return redirect(url_for('courses.show', course_title=course_name, user_id=user_id))


@posts_blueprint.route('/<course_name>/<user_id>/<post_id>/assignments', methods=['GET'])
@login_required
def show(course_name, user_id, post_id):
    user = User.get_or_none(User.id == user_id)
    print(user.id)
    current_course = Course.get_or_none(Course.title == course_name)
    thread = Thread.get_or_none(Thread.course_id == current_course.id)

    if user.role.role == 'Teacher':
        submitted_assignments = []
        for assignment in Assignment.select().where(Assignment.post_id == post_id):
            submitted_assignments.append(assignment)

    if user.role.role == 'Student':
        info = StudentCourse.get_or_none(StudentCourse.student_id == user.id, StudentCourse.course_name_id == current_course.id)
        submitted_assignments = Assignment.get_or_none(Assignment.info_id == info.id)

    assignment_post = []
    week_num = []
    i = 1

    for post in Post.select().where(Post.thread_id == thread.id):
        if post.file_path:
            assignment_post.append(post)
            week_num.append(i)

            i += 1

    grades = []
    for grade in Grade.select():
        grades.append(grade)


    assignment_week = dict(zip(week_num, assignment_post))
    print(str(assignment_week))

    # for assignment in Assignment.select().where()
    

    return render_template('posts/show.html', course_title=course_name, user_id=user_id, post_id=post_id, assignment_week=assignment_week, submitted_assignments=submitted_assignments, grades=grades)
        
    # is_student= user.role == "student"