from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from mongoengine.errors import NotUniqueError
from flask_mail import Mail, Message
import secrets
from flask import session
from models.job import Job




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


@main_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password_request():
    from app import mail  
    if request.method == 'POST':
        email = request.form.get('email')
        user = users_collection.find_one({'email': email.lower()})
        if user:
            # Generate a reset token
            reset_token = secrets.token_urlsafe(16)
            user_id = str(user['_id'])

            # Save the reset token to the user document
            users_collection.update_one({'_id': user['_id']}, {'$set': {'reset_token': reset_token}})

            # Send the reset email
            reset_link = url_for('main_bp.reset_password', token=reset_token, _external=True)
            msg = Message('Password Reset Request', sender='your-email@example.com', recipients=[email])
            msg.body = f'To reset your password, visit the following link:\n\n{reset_link}\n\nIf you did not make this request, simply ignore this email.'
            mail.send(msg)

            flash('An email has been sent with instructions to reset your password.', 'info')
            return redirect(url_for('main_bp.login'))

        flash('No account found with that email address.', 'error')
        return redirect(url_for('main_bp.reset_password_request'))

    return render_template('resetPasswordRequest.html')

@main_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = users_collection.find_one({'reset_token': token})
    if user:
        if request.method == 'POST':
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')

            if new_password == confirm_password:
                # Hash the new password and update the user document
                hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
                
                # Update the user document with the new password and reset_token set to None
                users_collection.update_one({'_id': user['_id']}, {'$set': {'password': hashed_password, 'reset_token': None}})

                flash('Your password has been reset successfully. You can now log in with your new password.', 'success')
                return redirect(url_for('main_bp.login'))

            flash('Passwords do not match.', 'error')
            return redirect(url_for('main_bp.reset_password', token=token))

        return render_template('resetPassword.html', token=token)

    flash('Invalid or expired reset token.', 'error')
    return redirect(url_for('main_bp.reset_password_request'))


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
            flash ('Email already exists. Please use a different email.')
            return render_template('signUp.html')

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
            
            # Store the user's role in the session
            session['user_role'] = user_obj.role

            # Redirect to the appropriate page based on the user's role
            return redirect(url_for('main_bp.admin_dashboard' if current_user.role == 'Admin' else 'main_bp.user_dashboard'))

        flash('Invalid email or password', 'error')
        return redirect(url_for('main_bp.login'))

    # Handle GET request (e.g., if someone tries to access the route directly without submitting the form)
    return render_template('login.html')

@main_bp.route('/Dashboard')
@login_required
def dashboard():
    user_role = session.get('user_role', 'User')  # Get the user's role from the session

    if user_role == 'Admin':
        return render_template('adminDashboard.html')  # Render the admin dashboard template
    else:
        return render_template('userDashboard.html')  # Render the user dashboard template


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

@main_bp.route('/Update-Careers', methods=['POST'])
def updateCareers():
    if request.method == 'POST':
        title = request.form.get('title')
        location = request.form.get('location')
        job_type = request.form.get('type')
        description = request.form.get('description')

        # Validate the form data as needed

        # Create a new job and save it to the database
        new_job = Job(
            title=title,
            location=location,
            type=job_type,
            description=description
        )
        new_job.save()

        # Serialize the new job
        serialized_job = {
            'id': str(new_job.id),
            'title': new_job.title,
            'location': new_job.location,
            'type': new_job.type,
            'description': new_job.description
            # Add more fields as needed
        }

        # If it's an AJAX request, return JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify(success=True, job=serialized_job)

    # If it's a regular form submission or another case, render HTML
    jobs = Job.objects()
    return render_template('updateCareers.html', jobs=jobs)


@main_bp.route('/Careers')
def careers():
    jobs = Job.objects()
    return render_template('careers.html', jobs=jobs)

@main_bp.route('/Update-Career-Page')
@login_required
def updateCareer():
    jobs = Job.objects()
    return render_template('updateCareers.html',jobs=jobs)

@main_bp.route('/delete_job/<job_id>', methods=['POST'])
@login_required
def delete_job(job_id):
    job = Job.objects(id=job_id).first()
    if job:
        job.delete()
        # Redirect to the updateCareers page after successful deletion
        return redirect(url_for('main_bp.updateCareer'))
    return jsonify(success=False, error='Job not found'), 404