from flask import Blueprint, render_template, request, redirect, url_for, flash, session,abort,jsonify
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
from app import app

# Twilio
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant


conferences_blueprint = Blueprint('conferences',
                            __name__,
                            template_folder='templates')

@conferences_blueprint.route('/', methods=['GET'])
def index():
    return render_template('conferences/video_call.html')

@conferences_blueprint.route('/login', methods=['POST'])
def login():
    print("******************************************************************kjhaugyf")
    # username = request.form.get('username')
    username = request.get_json(force=True).get('username')
    # username = request.form.get('username')
    if not username:
        abort(401)

    twilio_account_sid = app.config.get('TWILIO_ACCOUNT_SID')
    twilio_api_key_sid = app.config.get('TWILIO_API_KEY_SID')
    twilio_api_key_secret = app.config.get('TWILIO_API_KEY_SECRET')

    token = AccessToken(twilio_account_sid, twilio_api_key_sid,
                        twilio_api_key_secret, identity=username)
    token.add_grant(VideoGrant(room='My Room'))
    my_token = token.to_jwt().decode()
    print(my_token)
    token_dict = {'token': my_token }
    print(jsonify(token_dict))
    return jsonify(token_dict)