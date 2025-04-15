from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from backend.db_connection import db

rsvp = Blueprint("rsvps", __name__)

