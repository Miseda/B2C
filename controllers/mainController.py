from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from mongoengine.errors import NotUniqueError

main_bp = Blueprint('main_bp', __name__)

from mongoengine import connect

connect(db='B2C', host='mongodb+srv://B2C:12345@b2c.gxyirft.mongodb.net/?retryWrites=true&w=majority')

# Create a MongoDB client
client = MongoClient('mongodb+srv://B2C:12345@b2c.gxyirft.mongodb.net/?retryWrites=true&w=majority')

# Access the database and collection
db = client['B2C']  
users_collection = db['user']  

# Create an instance of the Bcrypt class
bcrypt = Bcrypt()

@main_bp.route('/SignUp', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form['fullName']
        phone_number = request.form['phone_number']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']
        
        # Check if a user with the same email already exists
        existing_user = users_collection.find_one({'email': email})
        if existing_user:
            error = 'Email already exists. Please use a different email.'
            return render_template('signUp.html', error=error)

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('main_bp.signup'))
        
        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create a new user
        new_user = User(
            full_name=full_name,
            phone_number=phone_number,
            email=email.lower(),
            password=hashed_password,
            role='User'
        )
        new_user.save()

        flash('Account created successfully. You can now log in.', 'success')
        return redirect(url_for('main_bp.login'))

    # Handle GET request (e.g., if someone tries to access the route directly without submitting the form)
    return render_template('signUp.html')


@main_bp.route('/Login', methods=['POST', 'GET'])
def login_post():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Find the user by email
        user = users_collection.find_one({'email': email.lower()})

        # Check if the user exists and the password is correct
        if user and bcrypt.check_password_hash(user.get('password', ''), password):
            user_obj = User.objects.get(id=str(user['_id']))  # Retrieve the User object based on the ObjectId
            login_user(user_obj)

            # Redirect to the appropriate page based on the user's role
            return redirect(url_for('main_bp.admin_dashboard' if current_user.role == 'Admin' else 'main_bp.user_dashboard'))

        flash('Invalid email or password', 'error')
        return redirect(url_for('main_bp.login'))

    # Handle GET request (e.g., if someone tries to access the route directly without submitting the form)
    return render_template('login.html')



@main_bp.route('/InsertAdmin')  # This route is just for one-time use to insert the admin user
def insert_admin():
    # Hash the admin password
    hashed_admin_password = bcrypt.generate_password_hash('Batanai2Create2023!').decode('utf-8')

    # Insert Admin User
    admin_user = User(
        full_name="Admin",
        phone_number="Admin Phone",
        email="admin@b2c.com",
        password=hashed_admin_password,
        role='Admin'
    )
    try:
        admin_user.save()
    except NotUniqueError:
        flash('Admin already exists.', 'error')
    return redirect(url_for('landing_page'))

@main_bp.route('/aboutUs')
def aboutUs():
    return render_template('aboutUs.html')

@main_bp.route('/Application-Development')
def appDev():
    return render_template('appDev.html')

@main_bp.route('/IT-Infrastructure')
def IT():
    return render_template('IT.html')

@main_bp.route('/System-Integration')
def sys():
    return render_template('sys.html')

@main_bp.route('/Careers')
def careers():
    return render_template('careers.html')

@main_bp.route('/Contact-Us')
def contact():
    return render_template('contactUs.html')

@main_bp.route('/Login')
def login():
    return render_template('login.html')

@main_bp.route('/SignUp')
def signUp():
    return render_template('signUp.html')



@main_bp.route('/Logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main_bp.login'))

@main_bp.route('/Admin-Dashboard')
@login_required
def admin_dashboard():
    if current_user.email == 'admin@b2c.com':
        return render_template('adminDashboard.html')  # Render the admin dashboard template
    else:
        flash('You do not have permission to access the admin dashboard.', 'error')
        return redirect(url_for('main_bp.landing_page'))

@main_bp.route('/User-Dashboard')
@login_required
def user_dashboard():
    return render_template('userDashboard.html')  # Render the user dashboard template

