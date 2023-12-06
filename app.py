from flask import Flask
from mongoengine import connect
from flask import Blueprint, render_template
from controllers.mainController import main_bp  # Import the main_bp Blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['MONGODB_SETTINGS'] = {
    'db': 'B2C',
    'host': 'mongodb+srv://B2C:12345@b2c.gxyirft.mongodb.net/?retryWrites=true&w=majority',
}

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
