from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
import re
from flask_login import login_user, logout_user, login_required, current_user
from next_learning_web.util.helpers import upload_file_to_s3
from werkzeug import secure_filename

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
    print(params.get("role"))
    new_user = User(username=params.get("username"), email=params.get("email"), password=params.get("password"), role = params.get("role"))
  
    if new_user.save():
        flash("Successfully Signed Up!","success")
        return redirect(url_for("users.show", username=new_user.username))  # then redirect to profile page
    else:
        flash(new_user.errors, "danger")
        return redirect(url_for("users.new"))


@users_blueprint.route('/<username>', methods=["GET"])  # user profile page
@login_required   # only can access this route after signed in
def show(username):
    user = User.get_or_none(User.username == username) # check whether user exist in database
    if user:
        return render_template("users/show.html",user=user)
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

            if len(password) > 0:
                user.password = password
            
            if user.save():
                flash("Successfully updated user!")
                return redirect(url_for("users.show", username=user.username))
            else:
                flash("Unable to edit!")
                for err in user.errors:
                    flash(err)
                return redirect(url_for("users.edit", id=user.id))
        else:
            flash("Cannot edit users other than yourself!")
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
                flash("No file provided!")
                return redirect(url_for("users.edit", id=id))

            file = request.files["profile_image"]
            file.filename = secure_filename(file.filename)
            image_path = upload_file_to_s3(file,user.username )
            
            user.image_path = image_path
            if user.save():
                return redirect(url_for("users.show", username=user.username))
            else:
                flash("Could not upload image. Please try again")
                return redirect(url_for("users.edit", id=id))       
        else:
            flash("Cannot edit users other than yourself!")
            return redirect(url_for("users.show", username=user.username))
    else:
        flash("No such user!")
        redirect(url_for("home"))
