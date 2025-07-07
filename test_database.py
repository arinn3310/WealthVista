import unittest
from datetime import datetime
from core import app
from db import db
from models import CurrencyRate, StockIndex, CommodityPrice, CryptoPrice, NewsItem, StockData

class DatabaseTestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            # Use existing db instance, no init_app call here
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_database_connection(self):
        with app.app_context():
            # Test if tables exist by querying
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            self.assertIn('currency_rates', tables)
            self.assertIn('stock_indices', tables)

    def test_currency_rate_crud(self):
        with app.app_context():
            # Create
            cr = CurrencyRate(symbol='USD', rate=1.0, change_percent=0.0)
            db.session.add(cr)
            db.session.commit()

            # Read
            cr_from_db = CurrencyRate.query.filter_by(symbol='USD').first()
            self.assertIsNotNone(cr_from_db)
            self.assertEqual(cr_from_db.rate, 1.0)

            # Update
            cr_from_db.rate = 1.1
            db.session.commit()
            updated_cr = CurrencyRate.query.filter_by(symbol='USD').first()
            self.assertEqual(updated_cr.rate, 1.1)

            # Delete
            db.session.delete(updated_cr)
            db.session.commit()
            deleted_cr = CurrencyRate.query.filter_by(symbol='USD').first()
            self.assertIsNone(deleted_cr)

    def test_stock_index_crud(self):
        with app.app_context():
            si = StockIndex(name='S&P 500', symbol='SPX', value=4000.0, change=10.0, change_percent=0.25)
            db.session.add(si)
            db.session.commit()

            si_from_db = StockIndex.query.filter_by(symbol='SPX').first()
            self.assertIsNotNone(si_from_db)
            self.assertEqual(si_from_db.value, 4000.0)

    def test_commodity_price_crud(self):
        with app.app_context():
            cp = CommodityPrice(name='Gold', symbol='XAU', price=1800.0, change_percent=0.5, unit='oz')
            db.session.add(cp)
            db.session.commit()

            cp_from_db = CommodityPrice.query.filter_by(symbol='XAU').first()
            self.assertIsNotNone(cp_from_db)
            self.assertEqual(cp_from_db.price, 1800.0)

    def test_crypto_price_crud(self):
        with app.app_context():
            crypto = CryptoPrice(symbol='BTC', name='Bitcoin', price_inr=3000000.0, change_percent=2.0)
            db.session.add(crypto)
            db.session.commit()

            crypto_from_db = CryptoPrice.query.filter_by(symbol='BTC').first()
            self.assertIsNotNone(crypto_from_db)
            self.assertEqual(crypto_from_db.price_inr, 3000000.0)

    def test_news_item_crud(self):
        with app.app_context():
            news = NewsItem(title='Market News', description='Stock market rises', url='http://news.com/article', source='NewsSource', published_at=datetime.utcnow())
            db.session.add(news)
            db.session.commit()

            news_from_db = NewsItem.query.filter_by(title='Market News').first()
            self.assertIsNotNone(news_from_db)
            self.assertEqual(news_from_db.source, 'NewsSource')

    def test_stock_data_crud(self):
        with app.app_context():
            stock = StockData(symbol='AAPL', name='Apple Inc.', price=150.0, change=1.5, change_percent=1.0)
            db.session.add(stock)
            db.session.commit()

            stock_from_db = StockData.query.filter_by(symbol='AAPL').first()
            self.assertIsNotNone(stock_from_db)
            self.assertEqual(stock_from_db.price, 150.0)

if __name__ == '__main__':
    unittest.main()
