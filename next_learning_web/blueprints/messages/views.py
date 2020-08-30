from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from models.course import Course
from models.student_course import StudentCourse
from models.message import Message
import peewee as pw
import re
from flask_login import login_user, logout_user, login_required, current_user


messages_blueprint = Blueprint('messages',
                            __name__,
                            template_folder='templates')

@messages_blueprint.route('/show', methods=['GET'])
def show():
    return render_template('messages/show.html')
  

@messages_blueprint.route('/', methods=['POST'])
@login_required
def create():
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
        content = request.form.get("post_content")
        new_post = Post(post_content=content, thread=course_thread,user=user)
        new_post.save()
    
  
    course_posts = []

    # for post in Post.select().where(Post.thread_id == course_thread):
    #     course_posts.append(post)

    # course_posts.reverse()

    # return render_template('courses/show.html', course_title=course_name, course_posts=course_posts, id=id)
    return redirect(url_for('courses.show',course_title=course_name))
         
