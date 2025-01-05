from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from instance import config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config.Config)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Create the database tables if they don't exist. Run this code only once when first time you are running your code
    from .models import User, Blog
    with app.app_context():
        db.create_all()

        # Add demo user and admin if not already in the database
        demo_user = User.query.filter_by(username='demo@gunjan.com').first()
        if not demo_user:
            demo_user = User(username='demo@gunjan.com', role='user')
            demo_user.set_password('demo123')  # Set password hash
            db.session.add(demo_user)

        admin_user = User.query.filter_by(username='admin@gunjan.com').first()
        if not admin_user:
            admin_user = User(username='admin@gunjan.com', role='admin')
            admin_user.set_password('admin123')  # Set password hash
            db.session.add(admin_user)

        # Creating demo blog posts
        post_check = Blog.query.first()
        if not post_check:
            post1 = Blog(title="First Blog Post", content="This is the content of the first blog post.")
            post2 = Blog(title="Second Blog Post", content="This is the content of the second blog post.")
            post3 = Blog(title="Third Blog Post", content="This is the content of the third blog post.")

            # Add posts to the database
            db.session.add(post1)
            db.session.add(post2)
            db.session.add(post3)

        db.session.commit()

    from app.routes import main
    app.register_blueprint(main)

    return app