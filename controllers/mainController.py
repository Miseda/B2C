from flask import Blueprint, render_template

main_bp = Blueprint('main_bp', __name__)

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
