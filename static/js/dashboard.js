// Dashboard JavaScript for Indian Financial Dashboard

class FinancialDashboard {
    constructor() {
        this.refreshInterval = 15 * 60 * 1000; // 15 minutes
        this.refreshTimer = null;
        this.lastUpdateTime = null;
        this.countdownTimer = null;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.loadAllData();
        this.startAutoRefresh();
        this.updateLastUpdateTime();
    }
    
    setupEventListeners() {
        // Theme toggle
        document.getElementById('themeToggle').addEventListener('click', this.toggleTheme.bind(this));
        
        // Currency converter inputs
        document.getElementById('convertAmount').addEventListener('input', this.debounce(this.convertCurrency.bind(this), 500));
        document.getElementById('fromCurrency').addEventListener('change', this.convertCurrency.bind(this));
        document.getElementById('toCurrency').addEventListener('change', this.convertCurrency.bind(this));
        
        // Auto-convert on page load
        setTimeout(() => this.convertCurrency(), 1000);
    }
    
    async loadAllData() {
        this.updateDataStatus('Loading data...', 'loading');
        
        try {
            await Promise.all([
                this.loadCurrencyRates(),
                this.loadStockIndices(),
                this.loadCommodityPrices(),
                this.loadCryptoPrices(),
                this.loadFinancialNews(),
                this.loadGainersLosers()
            ]);
            
            this.updateDataStatus('Data loaded successfully', 'success');
            this.lastUpdateTime = new Date();
            this.updateLastUpdateTime();
        } catch (error) {
            console.error('Error loading data:', error);
            this.updateDataStatus('Error loading data', 'error');
        }
    }
    
    async loadCurrencyRates() {
        try {
            const response = await fetch('/api/currency-rates');
            const data = await response.json();
            
            if (data.success) {
                this.renderCurrencyRates(data.data);
                this.updateQuickStats('currency', data.data);
            } else {
                this.renderError('currencyRatesContainer', 'Failed to load currency rates');
            }
        } catch (error) {
            console.error('Error loading currency rates:', error);
            this.renderError('currencyRatesContainer', 'Error loading currency rates');
        }
    }
    
    async loadStockIndices() {
        try {
            const response = await fetch('/api/stock-indices');
            const data = await response.json();
            
            if (data.success) {
                this.renderStockIndices(data.data);
                this.updateQuickStats('stocks', data.data);
            } else {
                this.renderError('stockIndicesContainer', 'Failed to load stock indices');
            }
        } catch (error) {
            console.error('Error loading stock indices:', error);
            this.renderError('stockIndicesContainer', 'Error loading stock indices');
        }
    }
    
    async loadCommodityPrices() {
        try {
            const response = await fetch('/api/commodity-prices');
            const data = await response.json();
            
            if (data.success) {
                this.renderCommodityPrices(data.data);
                this.updateQuickStats('commodities', data.data);
            } else {
                this.renderError('commodityPricesContainer', 'Failed to load commodity prices');
            }
        } catch (error) {
            console.error('Error loading commodity prices:', error);
            this.renderError('commodityPricesContainer', 'Error loading commodity prices');
        }
    }
    
    async loadCryptoPrices() {
        try {
            const response = await fetch('/api/crypto-prices');
            const data = await response.json();
            
            if (data.success) {
                this.renderCryptoPrices(data.data);
                this.updateQuickStats('crypto', data.data);
            } else {
                this.renderError('cryptoPricesContainer', 'Failed to load crypto prices');
            }
        } catch (error) {
            console.error('Error loading crypto prices:', error);
            this.renderError('cryptoPricesContainer', 'Error loading crypto prices');
        }
    }
    
    async loadFinancialNews() {
        try {
            const response = await fetch('/api/financial-news');
            const data = await response.json();
            
            if (data.success) {
                this.renderFinancialNews(data.data);
            } else {
                this.renderError('financialNewsContainer', 'Failed to load financial news');
            }
        } catch (error) {
            console.error('Error loading financial news:', error);
            this.renderError('financialNewsContainer', 'Error loading financial news');
        }
    }
    
    async loadGainersLosers() {
        try {
            const response = await fetch('/api/gainers-losers');
            const data = await response.json();
            
            if (data.success) {
                this.renderGainersLosers(data.data);
            } else {
                this.renderError('topGainersContainer', 'Failed to load top gainers');
                this.renderError('topLosersContainer', 'Failed to load top losers');
            }
        } catch (error) {
            console.error('Error loading gainers/losers:', error);
            this.renderError('topGainersContainer', 'Error loading top gainers');
            this.renderError('topLosersContainer', 'Error loading top losers');
        }
    }
    
    renderCurrencyRates(rates) {
        const container = document.getElementById('currencyRatesContainer');
        if (!rates || Object.keys(rates).length === 0) {
            container.innerHTML = '<p class="text-muted text-center">No currency data available</p>';
            return;
        }
        
        const html = Object.entries(rates).map(([symbol, rate]) => `
            <div class="d-flex justify-content-between align-items-center py-2 border-bottom">
                <div>
                    <strong>${symbol}</strong>
                    <small class="text-muted d-block">${new Date(rate.last_updated).toLocaleString()}</small>
                </div>
                <div class="text-end">
                    <div class="h6 mb-0">₹${rate.rate.toFixed(2)}</div>
                    <small class="${rate.change_percent >= 0 ? 'text-success' : 'text-danger'}">
                        ${rate.change_percent >= 0 ? '+' : ''}${rate.change_percent.toFixed(2)}%
                    </small>
                </div>
            </div>
        `).join('');
        
        container.innerHTML = html;
    }
    
    renderStockIndices(indices) {
        const container = document.getElementById('stockIndicesContainer');
        if (!indices || Object.keys(indices).length === 0) {
            container.innerHTML = '<p class="text-muted text-center">No stock data available</p>';
            return;
        }
        
        const html = Object.entries(indices).map(([name, index]) => `
            <div class="d-flex justify-content-between align-items-center py-2 border-bottom">
                <div>
                    <strong>${index.name}</strong>
                    <small class="text-muted d-block">${new Date(index.last_updated).toLocaleString()}</small>
                </div>
                <div class="text-end">
                    <div class="h6 mb-0">${index.value.toFixed(2)}</div>
                    <small class="${index.change_percent >= 0 ? 'text-success' : 'text-danger'}">
                        ${index.change >= 0 ? '+' : ''}${index.change.toFixed(2)} 
                        (${index.change_percent >= 0 ? '+' : ''}${index.change_percent.toFixed(2)}%)
                    </small>
                </div>
            </div>
        `).join('');
        
        container.innerHTML = html;
    }
    
    renderCommodityPrices(commodities) {
        const container = document.getElementById('commodityPricesContainer');
        if (!commodities || Object.keys(commodities).length === 0) {
            container.innerHTML = '<p class="text-muted text-center">No commodity data available</p>';
            return;
        }
        
        const html = Object.entries(commodities).map(([symbol, commodity]) => `
            <div class="d-flex justify-content-between align-items-center py-2 border-bottom">
                <div>
                    <strong>${commodity.name}</strong>
                    <small class="text-muted d-block">${commodity.unit}</small>
                </div>
                <div class="text-end">
                    <div class="h6 mb-0">₹${commodity.price.toFixed(2)}</div>
                    <small class="${commodity.change_percent >= 0 ? 'text-success' : 'text-danger'}">
                        ${commodity.change_percent >= 0 ? '+' : ''}${commodity.change_percent.toFixed(2)}%
                    </small>
                </div>
            </div>
        `).join('');
        
        container.innerHTML = html;
    }
    
    renderCryptoPrices(cryptos) {
        const container = document.getElementById('cryptoPricesContainer');
        if (!cryptos || Object.keys(cryptos).length === 0) {
            container.innerHTML = '<p class="text-muted text-center">No crypto data available</p>';
            return;
        }
        
        const html = Object.entries(cryptos).map(([symbol, crypto]) => `
            <div class="d-flex justify-content-between align-items-center py-2 border-bottom">
                <div>
                    <strong>${crypto.name}</strong>
                    <small class="text-muted d-block">${crypto.symbol}</small>
                </div>
                <div class="text-end">
                    <div class="h6 mb-0">₹${crypto.price_inr.toLocaleString()}</div>
                    <small class="${crypto.change_percent >= 0 ? 'text-success' : 'text-danger'}">
                        ${crypto.change_percent >= 0 ? '+' : ''}${crypto.change_percent.toFixed(2)}%
                    </small>
                </div>
            </div>
        `).join('');
        
        container.innerHTML = html;
    }
    
    renderFinancialNews(news) {
        const container = document.getElementById('financialNewsContainer');
        if (!news || news.length === 0) {
            container.innerHTML = '<p class="text-muted text-center">No news available</p>';
            return;
        }
        
        const html = news.slice(0, 5).map(article => `
            <div class="news-item">
                <h6 class="mb-1">
                    <a href="${article.url}" target="_blank" class="text-decoration-none">
                        ${article.title}
                    </a>
                </h6>
                <p class="text-muted mb-1">${article.description || 'No description available'}</p>
                <small class="text-muted">
                    <i class="fas fa-clock me-1"></i>
                    ${new Date(article.published_at).toLocaleString()} 
                    • ${article.source}
                </small>
            </div>
        `).join('');
        
        container.innerHTML = html;
    }
    
    renderGainersLosers(data) {
        this.renderStockList('topGainersContainer', data.gainers, 'success');
        this.renderStockList('topLosersContainer', data.losers, 'danger');
    }
    
    renderStockList(containerId, stocks, colorClass) {
        const container = document.getElementById(containerId);
        if (!stocks || stocks.length === 0) {
            container.innerHTML = '<p class="text-muted text-center">No data available</p>';
            return;
        }
        
        const html = stocks.map(stock => `
            <div class="d-flex justify-content-between align-items-center py-2 border-bottom">
                <div>
                    <strong>${stock.symbol}</strong>
                    <small class="text-muted d-block">${stock.name}</small>
                </div>
                <div class="text-end">
                    <div class="h6 mb-0">₹${stock.price.toFixed(2)}</div>
                    <small class="text-${colorClass}">
                        ${stock.change >= 0 ? '+' : ''}${stock.change.toFixed(2)} 
                        (${stock.change_percent >= 0 ? '+' : ''}${stock.change_percent.toFixed(2)}%)
                    </small>
                </div>
            </div>
        `).join('');
        
        container.innerHTML = html;
    }
    
    updateQuickStats(type, data) {
        switch (type) {
            case 'currency':
                if (data['USD-INR']) {
                    const usdInr = data['USD-INR'];
                    document.getElementById('usdInrRate').textContent = `₹${usdInr.rate.toFixed(2)}`;
                    document.getElementById('usdInrChange').textContent = `${usdInr.change_percent >= 0 ? '+' : ''}${usdInr.change_percent.toFixed(2)}%`;
                    document.getElementById('usdInrChange').className = usdInr.change_percent >= 0 ? 'text-success' : 'text-danger';
                }
                break;
            case 'stocks':
                if (data['NIFTY 50']) {
                    const nifty = data['NIFTY 50'];
                    document.getElementById('niftyValue').textContent = nifty.value.toFixed(2);
                    document.getElementById('niftyChange').textContent = `${nifty.change >= 0 ? '+' : ''}${nifty.change.toFixed(2)} (${nifty.change_percent >= 0 ? '+' : ''}${nifty.change_percent.toFixed(2)}%)`;
                    document.getElementById('niftyChange').className = nifty.change_percent >= 0 ? 'text-success' : 'text-danger';
                }
                break;
            case 'commodities':
                if (data['GOLD']) {
                    const gold = data['GOLD'];
                    document.getElementById('goldPrice').textContent = `₹${gold.price.toFixed(0)}`;
                }
                break;
            case 'crypto':
                if (data['BITCOIN']) {
                    const bitcoin = data['BITCOIN'];
                    document.getElementById('bitcoinPrice').textContent = `₹${bitcoin.price_inr.toLocaleString()}`;
                    document.getElementById('bitcoinChange').textContent = `${bitcoin.change_percent >= 0 ? '+' : ''}${bitcoin.change_percent.toFixed(2)}%`;
                    document.getElementById('bitcoinChange').className = bitcoin.change_percent >= 0 ? 'text-success' : 'text-danger';
                }
                break;
        }
    }
    
    async convertCurrency() {
        const amount = parseFloat(document.getElementById('convertAmount').value) || 1;
        const fromCurrency = document.getElementById('fromCurrency').value;
        const toCurrency = document.getElementById('toCurrency').value;
        
        try {
            const response = await fetch(`/api/convert?from=${fromCurrency}&to=${toCurrency}&amount=${amount}`);
            const data = await response.json();
            
            if (data.success) {
                const result = data.data;
                document.getElementById('conversionResult').classList.remove('d-none');
                document.getElementById('conversionText').innerHTML = `
                    <strong>${result.amount} ${result.from_currency}</strong> = 
                    <strong>${result.converted_amount.toFixed(2)} ${result.to_currency}</strong>
                    <br><small>Exchange rate: 1 ${result.from_currency} = ${result.rate.toFixed(4)} ${result.to_currency}</small>
                `;
            } else {
                document.getElementById('conversionResult').classList.add('d-none');
            }
        } catch (error) {
            console.error('Error converting currency:', error);
            document.getElementById('conversionResult').classList.add('d-none');
        }
    }
    
    renderError(containerId, message) {
        const container = document.getElementById(containerId);
        container.innerHTML = `
            <div class="error-state">
                <i class="fas fa-exclamation-triangle"></i>
                <h6>Error</h6>
                <p>${message}</p>
            </div>
        `;
    }
    
    updateDataStatus(message, type) {
        const statusElement = document.getElementById('dataStatus');
        const refreshIcon = document.getElementById('refreshIcon');
        
        statusElement.textContent = message;
        
        if (type === 'loading') {
            refreshIcon.classList.add('refresh-spin');
            statusElement.className = 'status-warning';
        } else if (type === 'success') {
            refreshIcon.classList.remove('refresh-spin');
            statusElement.className = 'status-online';
        } else if (type === 'error') {
            refreshIcon.classList.remove('refresh-spin');
            statusElement.className = 'status-offline';
        }
    }
    
    updateLastUpdateTime() {
        const timeElement = document.getElementById('lastUpdateTime');
        if (this.lastUpdateTime) {
            timeElement.textContent = this.lastUpdateTime.toLocaleString();
        }
    }
    
    startAutoRefresh() {
        this.startCountdown();
        this.refreshTimer = setInterval(() => {
            this.loadAllData();
            this.startCountdown();
        }, this.refreshInterval);
    }
    
    startCountdown() {
        const countdownElement = document.getElementById('refreshCountdown');
        let timeLeft = this.refreshInterval / 1000; // Convert to seconds
        
        if (this.countdownTimer) {
            clearInterval(this.countdownTimer);
        }
        
        this.countdownTimer = setInterval(() => {
            const minutes = Math.floor(timeLeft / 60);
            const seconds = timeLeft % 60;
            countdownElement.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
            
            if (timeLeft <= 0) {
                clearInterval(this.countdownTimer);
                countdownElement.textContent = 'Refreshing...';
            }
            
            timeLeft--;
        }, 1000);
    }
    
    toggleTheme() {
        const html = document.documentElement;
        const themeIcon = document.getElementById('themeIcon');
        const currentTheme = html.getAttribute('data-bs-theme');
        
        if (currentTheme === 'dark') {
            html.setAttribute('data-bs-theme', 'light');
            themeIcon.className = 'fas fa-moon';
            localStorage.setItem('theme', 'light');
        } else {
            html.setAttribute('data-bs-theme', 'dark');
            themeIcon.className = 'fas fa-sun';
            localStorage.setItem('theme', 'dark');
        }
    }
    
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}

// Global refresh functions
function refreshCurrencyData() {
    dashboard.loadCurrencyRates();
}

function refreshStockData() {
    dashboard.loadStockIndices();
}

function refreshCommodityData() {
    dashboard.loadCommodityPrices();
}

function refreshCryptoData() {
    dashboard.loadCryptoPrices();
}

function refreshNewsData() {
    dashboard.loadFinancialNews();
}

function convertCurrency() {
    dashboard.convertCurrency();
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Load saved theme
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-bs-theme', savedTheme);
    document.getElementById('themeIcon').className = savedTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    
    // Initialize dashboard
    window.dashboard = new FinancialDashboard();
});
