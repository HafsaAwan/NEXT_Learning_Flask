from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
import peewee as pw


assignments_blueprint = Blueprint('assignments',
                            __name__,
                            template_folder='templates')

@assignments_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('assignments/new.html')

@assignments_blueprint.route('/', methods=['POST'])
def create():
    pass

@assignments_blueprint.route('/<user_id>/upload', methods=['POST'])
def upload(user_id):
    pass
    # user = User.get_or_none(User.id == user_id)
    
    # if user:
    #     if current_user.id == int(user_id):
    #         # We check the request.files object for a user_file key. (user_file is the name of the file input on our form). If it's not there, we return an error message.
    #         if "assignment" not in request.files:
    #             flash("No file provided!")
    #             return redirect(url_for('assignments.new'))
            
    #         # If the key is in the object, we save it in a variable called file.
    #         file = request.files["assignment"]

    #         # we sanitize the filename using the secure_filename helper function provided by the werkzeurg.security module.
    #         file.filename = secure_filename(file.filename)

    #         # get path to image on S3 bucket using function in helper.py
    #         file_path = upload_file_to_s3(file, user.username)
            
    #         new_assignment = Assignment(user=user, image_url=image_path)
            
    #         if new_assignment.save():
    #             flash("Successfully uploaded!","success")
    #             # return redirect(url_for("users.show", username=user.username))  # then redirect to profile page
    #         else:
    #             flash("Upload failed :(  Please try again")
    #             return redirect(url_for('assignments.new'))
    #     else:
    #         flash("Cannot uplaod assignments for other users", "danger")
    #         return redirect(url_for('users.show', username = user.username))
            
    # else:
    #     flash("No user found!")
    #     return redirect(url_for('home'))