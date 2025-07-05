from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime

@dataclass
class CurrencyRate:
    symbol: str
    rate: float
    change_percent: float
    last_updated: datetime

@dataclass
class StockIndex:
    name: str
    symbol: str
    value: float
    change: float
    change_percent: float
    last_updated: datetime

@dataclass
class CommodityPrice:
    name: str
    symbol: str
    price: float
    change_percent: float
    unit: str
    last_updated: datetime

@dataclass
class CryptoPrice:
    symbol: str
    name: str
    price_inr: float
    change_percent: float
    last_updated: datetime

@dataclass
class NewsItem:
    title: str
    description: str
    url: str
    source: str
    published_at: datetime

@dataclass
class StockData:
    symbol: str
    name: str
    price: float
    change: float
    change_percent: float
