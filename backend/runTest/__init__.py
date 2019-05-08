from flask import Blueprint

run_test = Blueprint('run_test', __name__)

from . import views
