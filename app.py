import os
import config
from flask import Flask
from models.base_model import db
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from models.user import User
from flask_jwt_extended import JWTManager
# Twilio
from dotenv import load_dotenv
# from flask import Flask, render_template, request, abort
# from twilio.jwt.access_token import AccessToken
# from twilio.jwt.access_token.grants import VideoGrant
load_dotenv()

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'next_learning_web')

app = Flask('NEXT_Learning', root_path=web_dir)

csrf = CSRFProtect(app)
jwt = JWTManager(app)

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

login_manager = LoginManager()
login_manager.init_app(app) # configure the app for flask-login

login_manager.login_view = "sessions.new"   # if user try to access login_required route without sign in, will redirect to `sessions.new`
login_manager.login_message = "Please log in before proceeding"
login_manager.login_message_category = "warning"


# This callback is used to reload the user object from the user ID stored in the session.
@login_manager.user_loader
def load_user(user_id):
    return User.get_or_none(User.id == user_id)


@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc

# Twilio
# @app.route('/login', methods=['POST'])
# def login():
#     username = request.get_json(force=True).get('username')
#     if not username:
#         abort(401)

#     token = AccessToken(twilio_account_sid, twilio_api_key_sid,
#                         twilio_api_key_secret, identity=username)
#     token.add_grant(VideoGrant(room='My Room'))

#     return {'token': token.to_jwt().decode()}