from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
from models.course import Course
from models.student_course import StudentCourse
from models.student_guardian import StudentGuardian
import peewee as pw
import re
from flask_login import login_user, logout_user, login_required, current_user
from next_learning_web.util.helpers import upload_file_to_s3
# from werkzeug import secure_filename

import peewee as pw

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    params = request.form
    # print(params.get("role"))
    
    new_user = User(first_name=params.get("first_name"), last_name=params.get("last_name"),username=params.get("username"), email=params.get("email"), password=params.get("password"), role = params.get("role"))
    
    if new_user.save():
        flash("Successfully Signed Up!","success")
        login_user(new_user)
        return redirect(url_for("users.show", username=new_user.username))  # then redirect to profile page
    else:
        flash(new_user.errors, "danger")
        return redirect(url_for("users.new"))


@users_blueprint.route('/<username>', methods=["GET"])  # user profile page
@login_required   # only can access this route after signed in
def show(username):
    user = User.get_or_none(User.username == username) # check whether user exist in database

    teacher_courses = []

    # get the courses taught by the current teacher
    for course in Course.select().where(Course.teacher_id == current_user.id):
        # print(course)
        teacher_courses.append(course)

    student_info = []
    student_courses = []

    # get all courses id enrolled by the current student
    for info in StudentCourse.select().where(StudentCourse.student_id == current_user.id):
        student_info.append(info)
    
    # get the info of the courses enrolled the current student
    for info in student_info:
        for course in Course.select().where(Course.id == info.course_name_id):
            student_courses.append(course)

    child_parent = []
    child_info = []

    # get all child id respective to the current guardian
    for student in StudentGuardian.select().where(StudentGuardian.guardian_id == current_user.id):
        child_parent.append(student)

    # get child info respective to current guardian
    for info in child_parent:
        for child in User.select().where(User.id == info.student_id):
            child_info.append(child)
            print(child.username)

    child_course = []
    course_info = []
    teacher_info = []

    # get all courses enrolled by the child respective to the current guardian
    for info in child_info:
        child_course_info = []
        for course in StudentCourse.select().where(StudentCourse.student_id == info.id):
            child_course_info.append(course)

        child_course.append(child_course_info)
        
    print(child_course)
        

    # get courses details enrolled by the child respective to the current guardian
    for info in child_course:
        course_child_details = []
        for course in info:
            for details in Course.select().where(Course.id == course.course_name_id):
                course_child_details.append(details)

        course_info.append(course_child_details)
    
    print(course_info)

    # get teacher details respective to courses enrolled by child respective to the current guardian
    dict_list = []
    for info in course_info:
        teacher_course_dict = {}
        for course in info:
            teacher_details = User.get_or_none(User.id == course.teacher_id)
            print(teacher_details.username)

            teacher_course_dict[teacher_details] = course

        dict_list.append(teacher_course_dict)
    
    print(dict_list)

    new_list = []
    i = len(child_info)
    
    for j in range(0,i):
        child_course_teacher = {}
        key = child_info[j]
        value = dict_list[j]
        child_course_teacher[key] = value
        print("child_courses_teacher: ", child_course_teacher)

        new_list.append(child_course_teacher)


    if user:
        return render_template("users/show.html", user=user, student_courses=student_courses, teacher_courses=teacher_courses, child_info=child_info, new_list=new_list)
    else:
        flash(f"No {username} user found.", "danger" )
        return redirect(url_for('home'))


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    user = User.get_or_none(User.id== id)
    if user:
        if current_user.id == int(id):
            return render_template("users/edit.html", user=user)
        else:
            flash("Cannot edit users other than yourself!")
            return redirect(url_for("users.show", username=user.username))
    else:
        flash("No such user!")
        redirect(url_for("home"))


@users_blueprint.route('/<id>', methods=['POST'])
@login_required
def update(id):
    user = User.get_or_none(User.id == id)
    if user:
        if current_user.id == int(id):
            params = request.form

            user.username = params.get("username")
            user.email = params.get("email")

            password = params.get("password")
            user.about_me = params.get("about")
            user.fav_quote = params.get("quote")

            if len(password) > 0:
                user.password = password
            

            if user.save():
                flash("Successfully updated user!","success")
                return redirect(url_for("users.show", username=user.username))
            else:
                flash("Unable to edit!")
                for err in user.errors:
                    flash(err)
                return redirect(url_for("users.edit", id=user.id))
        else:
            flash("Cannot edit users other than yourself!","danger")
            return redirect(url_for("users.show", username=user.username))
    else:
        flash("No such user!")
        redirect(url_for("home"))

@users_blueprint.route('/<id>/upload', methods=['POST'])
@login_required
def upload(id):
    user = User.get_or_none(User.id == id)
    if user:
        if current_user.id == int(id):
            
            if "profile_image" not in request.files:
                flash("No file provided!","danger")
                return redirect(url_for("users.edit", id=id))

            file = request.files["profile_image"]
            # file.filename = secure_filename(file.filename)
            image_path = upload_file_to_s3(file,user.username )
            
            user.image_path = image_path
            if user.save():
                return redirect(url_for("users.show", username=user.username))
            else:
                flash("Could not upload image. Please try again","danger")
                return redirect(url_for("users.edit", id=id))       
        else:
            flash("Cannot edit users other than yourself!","danger")
            return redirect(url_for("users.show", username=user.username))
    else:
        flash("No such user!")
        redirect(url_for("home"))


@users_blueprint.route('/<id>/register', methods=['POST'])
@login_required
def register(id):
    params = request.form

    username = params.get('username')

    student = User.get_or_none(User.username == username)

    if student.role_id == 1:
        info = StudentGuardian(student_id=student.id, guardian_id=current_user.id)
        info.save()
        flash("Successfully register a child!", "success")
        return redirect(url_for('users.show', username=current_user.username))
    else:
        flash("User is not a student!", "danger")
        return redirect(url_for('users.show', username=current_user.username))


@users_blueprint.route('/<id>/summary', methods=['GET'])
@login_required
def report(id):
    user = User.get_or_none(User.id == id)
    return render_template('progress_report.html', user=user)

        
 
    

