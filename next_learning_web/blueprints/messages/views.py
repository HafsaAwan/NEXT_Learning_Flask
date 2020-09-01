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

@messages_blueprint.route('/<to_user>/show', methods=['GET'])
def show(to_user):
    
    to_user_msgs =[]
    
    msg_records = Message.select().where(Message.from_user == current_user.id and Message.to_user == to_user)

    for msg in msg_records:
        to_user_msgs.append(msg)


    return render_template('messages/show.html', to_user=to_user ,to_user_msgs = to_user_msgs)


@messages_blueprint.route('/<to_user>', methods=['POST'])
@login_required
def create(to_user):

    user = User.get_or_none(User.id == current_user.id)

    message = request.form.get("message")

    new_message = Message(message=message, from_user = current_user.id, to_user=to_user)

    new_message.save()
  
    if new_message.save():
        flash("Successfully sent!","success")
        return redirect(url_for("messages.show", to_user=to_user))
    else:
        flash("failed to send message. Please try again")
        return redirect(url_for("messages.show", to_user=to_user))
    