from app import app, csrf
from flask import render_template
from next_learning_web.blueprints.users.views import users_blueprint
from next_learning_web.blueprints.sessions.views import sessions_blueprint
from next_learning_web.blueprints.assignments.views import assignments_blueprint
from next_learning_web.blueprints.courses.views import courses_blueprint
from next_learning_web.blueprints.posts.views import posts_blueprint
from next_learning_web.blueprints.messages.views import messages_blueprint
from next_learning_web.blueprints.conferences.views import conferences_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from next_learning_web.util.google_oauth import oauth

assets = Environment(app)
assets.register(bundles)

oauth.init_app(app)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(assignments_blueprint, url_prefix="/assignments")
app.register_blueprint(courses_blueprint, url_prefix="/courses")
app.register_blueprint(posts_blueprint, url_prefix="/posts")
app.register_blueprint(messages_blueprint, url_prefix="/messages")
app.register_blueprint(conferences_blueprint, url_prefix="/conferences")

csrf.exempt(conferences_blueprint)

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route("/")
def home():
    return render_template('home.html')

@app.route("/teaminfo")
def teaminfo():
    return render_template('teaminfo.html')