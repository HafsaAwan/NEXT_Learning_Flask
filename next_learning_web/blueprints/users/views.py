from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.user import User
import re
from flask_login import login_user, logout_user, login_required, current_user

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
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
