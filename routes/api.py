from flask import Blueprint, jsonify, request
from services.data_fetcher import DataFetcher
import logging
from core import cache

api_bp = Blueprint('api', __name__)

@api_bp.route('/currency-rates')
def get_currency_rates():
    """Get cached currency rates"""
    try:
        rates = cache.get('currency_rates') or {}
        return jsonify({
            'success': True,
            'data': {symbol: {
                'symbol': rate.symbol,
                'rate': rate.rate,
                'change_percent': rate.change_percent,
                'last_updated': rate.last_updated.isoformat()
            } for symbol, rate in rates.items()}
        })
    except Exception as e:
        logging.error(f"Error getting currency rates: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/stock-indices')
def get_stock_indices():
    """Get cached stock indices"""
    try:
        indices = cache.get('stock_indices') or {}
        return jsonify({
            'success': True,
            'data': {name: {
                'name': index.name,
                'symbol': index.symbol,
                'value': index.value,
                'change': index.change,
                'change_percent': index.change_percent,
                'last_updated': index.last_updated.isoformat()
            } for name, index in indices.items()}
        })
    except Exception as e:
        logging.error(f"Error getting stock indices: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/commodity-prices')
def get_commodity_prices():
    """Get cached commodity prices"""
    try:
        commodities = cache.get('commodity_prices') or {}
        return jsonify({
            'success': True,
            'data': {symbol: {
                'name': commodity.name,
                'symbol': commodity.symbol,
                'price': commodity.price,
                'change_percent': commodity.change_percent,
                'unit': commodity.unit,
                'last_updated': commodity.last_updated.isoformat()
            } for symbol, commodity in commodities.items()}
        })
    except Exception as e:
        logging.error(f"Error getting commodity prices: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/crypto-prices')
def get_crypto_prices():
    """Get cached crypto prices"""
    try:
        cryptos = cache.get('crypto_prices') or {}
        return jsonify({
            'success': True,
            'data': {symbol: {
                'symbol': crypto.symbol,
                'name': crypto.name,
                'price_inr': crypto.price_inr,
                'change_percent': crypto.change_percent,
                'last_updated': crypto.last_updated.isoformat()
            } for symbol, crypto in cryptos.items()}
        })
    except Exception as e:
        logging.error(f"Error getting crypto prices: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/financial-news')
def get_financial_news():
    """Get cached financial news"""
    try:
        news = cache.get('financial_news') or []
        return jsonify({
            'success': True,
            'data': [{
                'title': item.title,
                'description': item.description,
                'url': item.url,
                'source': item.source,
                'published_at': item.published_at.isoformat()
            } for item in news]
        })
    except Exception as e:
        logging.error(f"Error getting financial news: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/gainers-losers')
def get_gainers_losers():
    """Get cached top gainers and losers"""
    try:
        data = cache.get('gainers_losers') or {'gainers': [], 'losers': []}
        return jsonify({
            'success': True,
            'data': {
                'gainers': [{
                    'symbol': stock.symbol,
                    'name': stock.name,
                    'price': stock.price,
                    'change': stock.change,
                    'change_percent': stock.change_percent
                } for stock in data.get('gainers', [])],
                'losers': [{
                    'symbol': stock.symbol,
                    'name': stock.name,
                    'price': stock.price,
                    'change': stock.change,
                    'change_percent': stock.change_percent
                } for stock in data.get('losers', [])]
            }
        })
    except Exception as e:
        logging.error(f"Error getting gainers/losers: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@api_bp.route('/convert')
def convert_currency():
    """Convert currency using current rates"""
    try:
        from_currency = request.args.get('from', 'USD').upper()
        to_currency = request.args.get('to', 'INR').upper()
        amount = float(request.args.get('amount', 1))
        
        rates = cache.get('currency_rates') or {}
        conversion_key = f"{from_currency}-{to_currency}"
        
        if conversion_key in rates:
            rate = rates[conversion_key].rate
            converted_amount = amount * rate
            return jsonify({
                'success': True,
                'data': {
                    'from_currency': from_currency,
                    'to_currency': to_currency,
                    'amount': amount,
                    'converted_amount': converted_amount,
                    'rate': rate
                }
            })
        else:
            # Try reverse conversion if available
            reverse_key = f"{to_currency}-{from_currency}"
            if reverse_key in rates:
                rate = rates[reverse_key].rate
                if rate != 0:
                    converted_amount = amount / rate
                    return jsonify({
                        'success': True,
                        'data': {
                            'from_currency': from_currency,
                            'to_currency': to_currency,
                            'amount': amount,
                            'converted_amount': converted_amount,
                            'rate': 1 / rate
                        }
                    })
            
            # Fallback: if no conversion rate found, try to use 1:1 conversion for same currency
            if from_currency == to_currency:
            return jsonify({
                    'success': True,
                    'data': {
                        'from_currency': from_currency,
                        'to_currency': to_currency,
                        'amount': amount,
                        'converted_amount': amount,
                        'rate': 1.0
                    }
                })
            
            return jsonify({
                'success': False,
                'error': f"Conversion rate not available for {conversion_key} or {reverse_key}"
            }), 400

    except Exception as e:
        logging.error(f"Error converting currency: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
