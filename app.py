from flask import Flask, render_template
from mongoengine import connect
from controllers.mainController import main_bp  # Import the main_bp Blueprint
from flask_login import LoginManager
from models.user import User
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['MONGODB_SETTINGS'] = {
    'db': 'B2C',
    'host': 'mongodb+srv://B2C:12345@b2c.gxyirft.mongodb.net/?retryWrites=true&w=majority',
}




app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465  # Use port 465 for SSL
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'batanai2create@gmail.com'  # Replace with your Gmail email
app.config['MAIL_PASSWORD'] = 'gkzi ccfo rcep qgio'  # Replace with your Gmail password


mail = Mail(app)

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'main_bp.login'

@login_manager.user_loader
def load_user(user_id):
    return User.objects.get(id=user_id)


# Register blueprints
app.register_blueprint(main_bp)  # Register the main_bp Blueprint

@app.route('/')
def landing_page():
    return render_template('landingPage.html')

@app.route('/check_connection')
def check_connection():
    try:
        connect('B2C')
        print('Successfully connected to MongoDB!')
        return 'Successfully connected to MongoDB!'
    except Exception as e:
        print('Error connecting to MongoDB: {}'.format(str(e)))
        return 'Error connecting to MongoDB: {}'.format(str(e))
    


if __name__ == '__main__':
    app.run(debug=True)
