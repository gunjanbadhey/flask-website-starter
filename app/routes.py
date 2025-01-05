from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db, bcrypt
from app.models import User, Blog
from app.forms import LoginForm
from werkzeug.security import generate_password_hash


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html', title="Home")

@main.route('/about')
def about():
    return render_template('about.html', title="About Us")

@main.route('/contact')
def contact():
    return render_template('contact.html', title="Contact Us")

@main.route("/products")
def products():
    # Sample product data (replace with database or API logic)
    products = [
        {"name": "Product 1", "price": 29.99, "description": "Description for Product 1", "image": "https://via.placeholder.com/300x200"},
        {"name": "Product 2", "price": 49.99, "description": "Description for Product 2", "image": "https://via.placeholder.com/300x200"},
        {"name": "Product 3", "price": 69.99, "description": "Description for Product 3", "image": "https://via.placeholder.com/300x200"}
    ]
    
    return render_template("product.html", products=products)

@main.route('/services')
def service():
    # Example list of services (replace with real service data)
    services = [
        {"name": "Service 1", "description": "Description of Service 1", "image": "https://via.placeholder.com/300x200"},
        {"name": "Service 2", "description": "Description of Service 2", "image": "https://via.placeholder.com/300x200"},
        {"name": "Service 3", "description": "Description of Service 3", "image": "https://via.placeholder.com/300x200"}
    ]
    
    return render_template("service.html", services=services)

@main.route('/blog')
def blog():
    posts = Blog.query.all()  # Get all blog posts from the database
    return render_template("blog.html", posts=posts)

@main.route("/blog/<int:post_id>")
def post(post_id):
    post = Blog.query.get_or_404(post_id)  # Get the blog post by ID
    return render_template("post.html", post=post)

@main.route('/privacy')
def privacy_policy():
    return render_template('privacy_policy.html', title="Privacy Policy")

@main.route('/terms')
def terms_of_service():
    return render_template('terms_of_service.html', title="Terms of Service")

# In-memory demo user credentials (replace with database validation)
demo_user = {"email": "user@example.com", "password": "password123"}

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login failed. Check your credentials.', 'danger')
    return render_template('login.html', title="Login", form=form)

@main.route("/login2", methods=["GET", "POST"])
def login2():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        # Check credentials (replace with real user validation)
        if email == demo_user["email"] and password == demo_user["password"]:
            flash("Login successful!", "success")
            return redirect("/")
        else:
            flash("Invalid email or password. Please try again.", "danger")
    
    return render_template("login.html")

@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Check if user already exists
        user = User.query.filter_by(username=username).first()
        if user:
            flash("Username already exists. Please choose a different username.", "danger")
            return redirect(url_for('register'))

        # Create a new user
        new_user = User(username=username, role='user')
        new_user.set_password(password)  # Hash password
        db.session.add(new_user)
        db.session.commit()

        # Log the user in after successful registration
        login_user(new_user)

        flash("Your account has been created successfully!", "success")
        return redirect(url_for('index'))  # Redirect to homepage after registration

    return render_template("register.html")

@main.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for("index"))

