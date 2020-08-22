from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
import peewee as pw


courses_blueprint = Blueprint('courses',
                            __name__,
                            template_folder='templates')

@courses_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('courses/new.html')

@courses_blueprint.route('/', methods=['POST'])
def create():
    pass
