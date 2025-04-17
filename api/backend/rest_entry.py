import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask

from backend.db_connection import db
from backend.products.products_routes import products
from backend.simple.simple_routes import simple_routes
from backend.posts.post_routes import posts
# importing club from club.py
from backend.club.club_routes import club
# import feedback route from feedback.py to give feedback to HuskyPulse
from backend.feedback.feedback_routes import feedback
#importing the application route to get applications for clubs/events
from backend.application.application_routes import application_routes
# importing the comments routes for comments under a user
from backend.comment.comment_routes import comments
# importing the recommendations routefor recommendations for clubs
from backend.recommendations.recommendation_routes import recommendations
# importing the student routes for the student routes
from backend.student.student_routes import student
# importing the location routes for the location routes
from backend.location.location_routes import location
#importing the event route for the events
from backend.events.event_routes import event
from backend.simple.olivia_routes import bp as olivia_bp
from backend.rsvp.rsvp_routes import rsvp
from backend.student_events.student_events import student_events
from backend.simple.zoe_routes import bp as zoe_bp


from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)
    app.register_blueprint(zoe_bp)
    # Load environment variables
    # This function reads all the values from inside
    # the .env file (in the parent folder) so they
    # are available in this file.  See the MySQL setup 
    # commands below to see how they're being used.
    load_dotenv()

    # secret key that will be used for securely signing the session 
    # cookie and can be used for any other security related needs by 
    # extensions or your application
    # app.config['SECRET_KEY'] = 'someCrazyS3cR3T!Key.!'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # # these are for the DB object to be able to connect to MySQL. 
    # app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_USER'] = os.getenv('DB_USER').strip()
    app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_ROOT_PASSWORD').strip()
    app.config['MYSQL_DATABASE_HOST'] = os.getenv('DB_HOST').strip()
    app.config['MYSQL_DATABASE_PORT'] = int(os.getenv('DB_PORT').strip())
    app.config['MYSQL_DATABASE_DB'] = os.getenv('DB_NAME').strip()  # Change this to your DB name

    # Initialize the database object with the settings above. 
    app.logger.info('current_app(): starting the database connection')
    db.init_app(app)


    # Register the routes from each Blueprint with the app object
    # and give a url prefix to each
    app.logger.info('current_app(): registering blueprints with Flask app object.')  
    # Post routes 
    app.register_blueprint(posts, url_prefix = "/p")
    # registering club
    app.register_blueprint(club, url_prefix='/club')
    # registering feedback
    app.register_blueprint(feedback, url_prefix='/feedback')
    # registering the application blueprint
    app.register_blueprint(application_routes)
    # registering the comment blueprint
    app.register_blueprint(comments, url_prefix='/comments')
    # registering the recommendations blueprint
    app.register_blueprint(recommendations, url_prefix='/recommend')
    # registering the student blueprint
    app.register_blueprint(student, url_prefix='/student')
    #registering the location blueprint
    app.register_blueprint(location, url_prefix='/location')
    #registering the event blueprint
    app.register_blueprint(event, url_prefix='/event')
    app.register_blueprint(olivia_bp, url_prefix='/admin')
    app.register_blueprint(rsvp, url_prefix='/rsvp')
    app.register_blueprint(student_events, url_prefix="/student_event")
    

    # Don't forget to return the app object
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=4000)
