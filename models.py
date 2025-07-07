from datetime import datetime
from db import db

class CurrencyRate(db.Model):
    __tablename__ = 'currency_rates'
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    rate = db.Column(db.Float, nullable=False)
    change_percent = db.Column(db.Float, nullable=False)
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class StockIndex(db.Model):
    __tablename__ = 'stock_indices'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    value = db.Column(db.Float, nullable=False)
    change = db.Column(db.Float, nullable=False)
    change_percent = db.Column(db.Float, nullable=False)
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class CommodityPrice(db.Model):
    __tablename__ = 'commodity_prices'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float, nullable=False)
    change_percent = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class CryptoPrice(db.Model):
    __tablename__ = 'crypto_prices'
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price_inr = db.Column(db.Float, nullable=False)
    change_percent = db.Column(db.Float, nullable=False)
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class NewsItem(db.Model):
    __tablename__ = 'news_items'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    url = db.Column(db.String(255), nullable=False)
    source = db.Column(db.String(100), nullable=False)
    published_at = db.Column(db.DateTime, nullable=False)

class StockData(db.Model):
    __tablename__ = 'stock_data'
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    change = db.Column(db.Float, nullable=False)
    change_percent = db.Column(db.Float, nullable=False)
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
