from flask import Blueprint, render_template

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/aboutUs')
def aboutUs():
    return render_template('aboutUs.html')
