# app.py
from flask import Flask, render_template
from mongoengine import connect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['MONGODB_SETTINGS'] = {
    'db': 'B2C',  # Database name
    'host': 'mongodb+srv://B2C:12345@b2c.gxyirft.mongodb.net/?retryWrites=true&w=majority',
}

@app.route('/')
def landing_page():
    return render_template('landingPage.html')

@app.route('/check_connection')
def check_connection():
    try:
        # Access the MongoDB connection through mongoengine's connect function
        connect('B2C')
        print('Successfully connected to MongoDB!')
        return 'Successfully connected to MongoDB!'
    except Exception as e:
        print('Successfully connected to MongoDB!')
        return 'Error connecting to MongoDB: {}'.format(str(e))

if __name__ == '__main__':
    app.run(debug=True)

