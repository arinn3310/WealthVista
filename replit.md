# Indian Financial Dashboard

## Overview

This is a Flask-based financial dashboard application that provides real-time financial data for Indian markets. The application fetches and displays currency exchange rates, stock indices, commodity prices, cryptocurrency prices, and financial news. It uses a background scheduler to periodically update data and caches it for improved performance.

## System Architecture

### Backend Architecture
- **Framework**: Flask web framework with Python
- **Caching**: Flask-Caching with simple in-memory cache (15-minute timeout)
- **Scheduling**: APScheduler for background data fetching tasks
- **Data Models**: Dataclasses for type-safe data structures
- **Timezone**: Asia/Kolkata (IST) for localized timestamps

### Frontend Architecture
- **Template Engine**: Jinja2 (Flask's default)
- **CSS Framework**: Bootstrap 5 with dark theme
- **JavaScript**: Vanilla JS with Chart.js for data visualization
- **Icons**: Font Awesome for UI icons
- **Responsive Design**: Mobile-first approach with Bootstrap grid system

### API Design
- RESTful API endpoints under `/api` prefix
- JSON responses with standardized error handling
- Cached data serving to reduce external API calls

## Key Components

### Core Application (`app.py`)
- Flask application initialization
- Cache configuration with 15-minute timeout
- Background scheduler setup
- Blueprint registration for modular routing
- ProxyFix middleware for deployment behind proxies

### Data Layer (`models.py`)
- `CurrencyRate`: Exchange rate data with change percentages
- `StockIndex`: Stock market indices (NIFTY, SENSEX, etc.)
- `CommodityPrice`: Commodity pricing data
- `CryptoPrice`: Cryptocurrency prices in INR
- `NewsItem`: Financial news articles
- `StockData`: Individual stock information

### Data Fetching Service (`services/data_fetcher.py`)
- External API integration for financial data
- Alpha Vantage API for stock and currency data
- Exchange rate API for currency conversions
- News API for financial news
- Session management with proper headers

### Scheduler Service (`services/scheduler.py`)
- Background task management
- 15-minute interval data fetching
- Comprehensive error handling and logging
- Cache population for all data types

### Route Handlers
- **Main Routes** (`routes/main.py`): Web page rendering
- **API Routes** (`routes/api.py`): JSON API endpoints

## Data Flow

1. **Background Scheduler**: Runs every 15 minutes to fetch fresh data
2. **Data Fetcher**: Makes HTTP requests to external financial APIs
3. **Cache Layer**: Stores fetched data in memory for fast access
4. **API Endpoints**: Serve cached data to frontend
5. **Frontend**: Displays data with real-time updates and visualizations

## External Dependencies

### Third-party APIs
- **Alpha Vantage**: Stock market data and currency rates
- **Exchange Rate API**: Real-time currency conversion rates
- **News API**: Financial news articles

### Python Libraries
- **Flask**: Web framework
- **Flask-Caching**: Caching layer
- **APScheduler**: Background task scheduling
- **Requests**: HTTP client for API calls
- **Pytz**: Timezone handling

### Frontend Libraries
- **Bootstrap 5**: CSS framework
- **Chart.js**: Data visualization
- **Font Awesome**: Icon library

## Deployment Strategy

### Environment Configuration
- Environment variables for API keys (`ALPHA_VANTAGE_API_KEY`, `NEWS_API_KEY`)
- Configurable session secret key
- Debug mode configuration

### Production Considerations
- ProxyFix middleware for reverse proxy deployment
- Structured logging for monitoring
- Graceful scheduler shutdown on application exit
- Error handling and fallback mechanisms

### Scalability
- Simple cache suitable for single-instance deployment
- Can be upgraded to Redis for multi-instance scaling
- Stateless application design for horizontal scaling

## User Preferences

Preferred communication style: Simple, everyday language.

## Changelog

Changelog:
- July 05, 2025. Initial setup