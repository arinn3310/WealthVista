# routes/__init__.py
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/', endpoint='index')
def index():
    return render_template('index.html')

@main_bp.route('/currency', endpoint='currency')
def currency():
    return render_template('index.html', active_section='currency')

@main_bp.route('/stocks', endpoint='stocks')
def stocks():
    return render_template('index.html', active_section='stocks')

@main_bp.route('/commodities', endpoint='commodities')
def commodities():
    return render_template('index.html', active_section='commodities')

@main_bp.route('/crypto', endpoint='crypto')
def crypto():
    return render_template('index.html', active_section='crypto')

@main_bp.route('/news', endpoint='news')
def news():
    return render_template('index.html', active_section='news')
