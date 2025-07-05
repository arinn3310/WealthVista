import logging
from apscheduler.triggers.interval import IntervalTrigger
from services.data_fetcher import DataFetcher

def start_data_fetching(scheduler, cache):
    """Start background data fetching tasks"""
    data_fetcher = DataFetcher()
    
    def fetch_and_cache_all_data():
        """Fetch all financial data and cache it"""
        try:
            logging.info("Starting data fetch cycle...")
            
            # Fetch currency rates
            currencies = data_fetcher.fetch_currency_rates()
            cache.set('currency_rates', currencies)
            logging.info(f"Cached {len(currencies)} currency rates")
            
            # Fetch stock indices
            indices = data_fetcher.fetch_stock_indices()
            cache.set('stock_indices', indices)
            logging.info(f"Cached {len(indices)} stock indices")
            
            # Fetch commodity prices
            commodities = data_fetcher.fetch_commodity_prices()
            cache.set('commodity_prices', commodities)
            logging.info(f"Cached {len(commodities)} commodity prices")
            
            # Fetch crypto prices
            cryptos = data_fetcher.fetch_crypto_prices()
            cache.set('crypto_prices', cryptos)
            logging.info(f"Cached {len(cryptos)} crypto prices")
            
            # Fetch financial news
            news = data_fetcher.fetch_financial_news()
            cache.set('financial_news', news)
            logging.info(f"Cached {len(news)} news items")
            
            # Fetch top gainers/losers
            gainers_losers = data_fetcher.fetch_top_gainers_losers()
            cache.set('gainers_losers', gainers_losers)
            logging.info(f"Cached {len(gainers_losers.get('gainers', []))} gainers and {len(gainers_losers.get('losers', []))} losers")
            
            logging.info("Data fetch cycle completed successfully")
            
        except Exception as e:
            logging.error(f"Error in data fetch cycle: {e}")
    
    # Schedule data fetching every 15 minutes
    scheduler.add_job(
        func=fetch_and_cache_all_data,
        trigger=IntervalTrigger(minutes=15),
        id='fetch_financial_data',
        name='Fetch Financial Data',
        replace_existing=True
    )
    
    # Run once immediately
    fetch_and_cache_all_data()
