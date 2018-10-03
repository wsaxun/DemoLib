from flask import Blueprint

api_blueprint = Blueprint('api', __name__)

from .view import *
from .urls import *
