import requests
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional
import pytz
from models import CurrencyRate, StockIndex, CommodityPrice, CryptoPrice, NewsItem, StockData

IST = pytz.timezone('Asia/Kolkata')

class DataFetcher:
    def __init__(self):
        self.alpha_vantage_key = os.getenv("ALPHA_VANTAGE_API_KEY", "demo")
        self.news_api_key = os.getenv("NEWS_API_KEY", "demo")
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def fetch_currency_rates(self) -> Dict[str, CurrencyRate]:
        """Fetch USD to INR and other major currency rates"""
        try:
            # Using exchangerate-api.com (free tier)
            url = "https://api.exchangerate-api.com/v4/latest/USD"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            current_time = datetime.now(IST)
            currencies = {}
            
            # Get INR rate
            if 'rates' in data and 'INR' in data['rates']:
                inr_rate = data['rates']['INR']
                currencies['USD-INR'] = CurrencyRate(
                    symbol="USD-INR",
                    rate=inr_rate,
                    change_percent=0.0,  # API doesn't provide change
                    last_updated=current_time
                )
            
            # Get other major currencies to INR
            major_currencies = ['EUR', 'GBP', 'AED', 'SGD', 'JPY']
            for currency in major_currencies:
                if currency in data['rates']:
                    # Convert to INR rate
                    rate_to_inr = data['rates']['INR'] / data['rates'][currency]
                    currencies[f'{currency}-INR'] = CurrencyRate(
                        symbol=f"{currency}-INR",
                        rate=rate_to_inr,
                        change_percent=0.0,
                        last_updated=current_time
                    )
            
            return currencies
            
        except Exception as e:
            logging.error(f"Error fetching currency rates: {e}")
            return {}

    def fetch_stock_indices(self) -> Dict[str, StockIndex]:
        """Fetch major Indian stock indices"""
        try:
            # Using Yahoo Finance alternative API
            indices = {}
            current_time = datetime.now(IST)
            
            # Yahoo Finance symbols for Indian indices
            symbols = {
                'NIFTY 50': '^NSEI',
                'SENSEX': '^BSESN',
                'BANK NIFTY': '^NSEBANK'
            }
            
            for name, symbol in symbols.items():
                try:
                    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
                    response = self.session.get(url, timeout=10)
                    response.raise_for_status()
                    data = response.json()
                    
                    if 'chart' in data and data['chart']['result']:
                        result = data['chart']['result'][0]
                        meta = result['meta']
                        
                        current_price = meta.get('regularMarketPrice', 0)
                        prev_close = meta.get('previousClose', 0)
                        
                        if current_price and prev_close:
                            change = current_price - prev_close
                            change_percent = (change / prev_close) * 100
                            
                            indices[name] = StockIndex(
                                name=name,
                                symbol=symbol,
                                value=current_price,
                                change=change,
                                change_percent=change_percent,
                                last_updated=current_time
                            )
                except Exception as e:
                    logging.error(f"Error fetching {name}: {e}")
                    continue
            
            return indices
            
        except Exception as e:
            logging.error(f"Error fetching stock indices: {e}")
            return {}

    def fetch_commodity_prices(self) -> Dict[str, CommodityPrice]:
        """Fetch gold, silver, and oil prices"""
        try:
            commodities = {}
            current_time = datetime.now(IST)
            
            # Using metals-api.com for gold and silver (free tier)
            try:
                url = "https://api.metals.live/v1/spot"
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                if isinstance(data, list) and len(data) > 0:
                    for item in data:
                        if item.get('metal') == 'gold':
                            # Convert to INR per gram (price is usually in USD per troy ounce)
                            gold_usd_per_oz = item.get('price', 0)
                            # Get USD-INR rate for conversion
                            usd_inr_rate = 83.0  # Fallback rate
                            gold_inr_per_gram = (gold_usd_per_oz * usd_inr_rate) / 31.1035
                            
                            commodities['GOLD'] = CommodityPrice(
                                name="Gold",
                                symbol="GOLD",
                                price=gold_inr_per_gram,
                                change_percent=0.0,
                                unit="INR/gram",
                                last_updated=current_time
                            )
                        elif item.get('metal') == 'silver':
                            silver_usd_per_oz = item.get('price', 0)
                            usd_inr_rate = 83.0
                            silver_inr_per_gram = (silver_usd_per_oz * usd_inr_rate) / 31.1035
                            
                            commodities['SILVER'] = CommodityPrice(
                                name="Silver",
                                symbol="SILVER",
                                price=silver_inr_per_gram,
                                change_percent=0.0,
                                unit="INR/gram",
                                last_updated=current_time
                            )
            except Exception as e:
                logging.error(f"Error fetching metals prices: {e}")
            
            # Crude oil price from Alpha Vantage
            try:
                url = f"https://www.alphavantage.co/query?function=WTI&interval=daily&apikey={self.alpha_vantage_key}"
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                if 'data' in data and len(data['data']) > 0:
                    latest_oil = data['data'][0]
                    oil_usd = float(latest_oil.get('value', 0))
                    usd_inr_rate = 83.0
                    oil_inr = oil_usd * usd_inr_rate
                    
                    commodities['CRUDE_OIL'] = CommodityPrice(
                        name="Crude Oil",
                        symbol="CRUDE_OIL",
                        price=oil_inr,
                        change_percent=0.0,
                        unit="INR/barrel",
                        last_updated=current_time
                    )
            except Exception as e:
                logging.error(f"Error fetching crude oil price: {e}")
            
            return commodities
            
        except Exception as e:
            logging.error(f"Error fetching commodity prices: {e}")
            return {}

    def fetch_crypto_prices(self) -> Dict[str, CryptoPrice]:
        """Fetch cryptocurrency prices in INR"""
        try:
            # Using CoinGecko API (free tier)
            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {
                'ids': 'bitcoin,ethereum,binancecoin,cardano,solana,dogecoin,polygon,chainlink',
                'vs_currencies': 'inr',
                'include_24hr_change': 'true'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            current_time = datetime.now(IST)
            cryptos = {}
            
            crypto_names = {
                'bitcoin': 'Bitcoin',
                'ethereum': 'Ethereum',
                'binancecoin': 'BNB',
                'cardano': 'Cardano',
                'solana': 'Solana',
                'dogecoin': 'Dogecoin',
                'polygon': 'Polygon',
                'chainlink': 'Chainlink'
            }
            
            for crypto_id, crypto_name in crypto_names.items():
                if crypto_id in data:
                    crypto_data = data[crypto_id]
                    price_inr = crypto_data.get('inr', 0)
                    change_24h = crypto_data.get('inr_24h_change', 0)
                    
                    cryptos[crypto_id.upper()] = CryptoPrice(
                        symbol=crypto_id.upper(),
                        name=crypto_name,
                        price_inr=price_inr,
                        change_percent=change_24h,
                        last_updated=current_time
                    )
            
            return cryptos
            
        except Exception as e:
            logging.error(f"Error fetching crypto prices: {e}")
            return {}

    def fetch_financial_news(self) -> List[NewsItem]:
        """Fetch latest financial news"""
        try:
            # Using NewsAPI (free tier)
            url = "https://newsapi.org/v2/top-headlines"
            params = {
                'country': 'in',
                'category': 'business',
                'apiKey': self.news_api_key,
                'pageSize': 10
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            news_items = []
            if 'articles' in data:
                for article in data['articles'][:10]:
                    published_at = datetime.fromisoformat(
                        article['publishedAt'].replace('Z', '+00:00')
                    ).astimezone(IST)
                    
                    news_items.append(NewsItem(
                        title=article['title'],
                        description=article.get('description', ''),
                        url=article['url'],
                        source=article['source']['name'],
                        published_at=published_at
                    ))
            
            return news_items
            
        except Exception as e:
            logging.error(f"Error fetching financial news: {e}")
            return []

    def fetch_top_gainers_losers(self) -> Dict[str, List[StockData]]:
        """Fetch top gainers and losers from Indian stock market"""
        try:
            # Using Yahoo Finance API for Indian stocks
            gainers = []
            losers = []
            
            # Sample Indian stock symbols
            symbols = [
                'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'HINDUNILVR.NS',
                'ICICIBANK.NS', 'KOTAKBANK.NS', 'SBIN.NS', 'BHARTIARTL.NS', 'ITC.NS'
            ]
            
            stocks_data = []
            for symbol in symbols:
                try:
                    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
                    response = self.session.get(url, timeout=5)
                    response.raise_for_status()
                    data = response.json()
                    
                    if 'chart' in data and data['chart']['result']:
                        result = data['chart']['result'][0]
                        meta = result['meta']
                        
                        current_price = meta.get('regularMarketPrice', 0)
                        prev_close = meta.get('previousClose', 0)
                        
                        if current_price and prev_close:
                            change = current_price - prev_close
                            change_percent = (change / prev_close) * 100
                            
                            stock_data = StockData(
                                symbol=symbol,
                                name=meta.get('symbol', symbol),
                                price=current_price,
                                change=change,
                                change_percent=change_percent
                            )
                            stocks_data.append(stock_data)
                            
                except Exception as e:
                    logging.error(f"Error fetching {symbol}: {e}")
                    continue
            
            # Sort by change percentage
            stocks_data.sort(key=lambda x: x.change_percent, reverse=True)
            
            # Top 5 gainers and losers
            gainers = stocks_data[:5]
            losers = stocks_data[-5:]
            
            return {
                'gainers': gainers,
                'losers': losers
            }
            
        except Exception as e:
            logging.error(f"Error fetching top gainers/losers: {e}")
            return {'gainers': [], 'losers': []}
