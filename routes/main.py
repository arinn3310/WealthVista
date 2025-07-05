from flask import Blueprint, render_template
from app import cache

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@main_bp.route('/currency')
def currency():
    """Currency rates page"""
    return render_template('index.html', active_section='currency')

@main_bp.route('/stocks')
def stocks():
    """Stock indices page"""
    return render_template('index.html', active_section='stocks')

@main_bp.route('/commodities')
def commodities():
    """Commodity prices page"""
    return render_template('index.html', active_section='commodities')

@main_bp.route('/crypto')
def crypto():
    """Cryptocurrency prices page"""
    return render_template('index.html', active_section='crypto')

@main_bp.route('/news')
def news():
    """Financial news page"""
    return render_template('index.html', active_section='news')
