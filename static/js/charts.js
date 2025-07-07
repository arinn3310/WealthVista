// charts.js - Chart rendering functions for Indian Financial Dashboard

async function fetchData(url) {
    const response = await fetch(url);
    const data = await response.json();
    if (!data.success) {
        throw new Error(data.error || 'Failed to fetch data');
    }
    return data.data;
}

async function renderCurrencyRatesChart() {
    try {
        const data = await fetchData('/api/currency-rates');
        const labels = Object.keys(data);
        const rates = labels.map(symbol => data[symbol].rate);
        
        const ctx = document.getElementById('currencyRatesChart').getContext('2d');
        if (window.currencyRatesChartInstance) {
            window.currencyRatesChartInstance.destroy();
        }
        window.currencyRatesChartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Currency Rates',
                    data: rates,
                    backgroundColor: 'rgba(54, 162, 235, 0.7)'
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    } catch (error) {
        console.error('Error rendering currency rates chart:', error);
    }
}

async function renderStockIndicesChart() {
    try {
        const data = await fetchData('/api/stock-indices');
        const labels = Object.keys(data);
        const values = labels.map(name => data[name].value);
        
        const ctx = document.getElementById('stockIndicesChart').getContext('2d');
        if (window.stockIndicesChartInstance) {
            window.stockIndicesChartInstance.destroy();
        }
        window.stockIndicesChartInstance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Stock Indices',
                    data: values,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    fill: false,
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: false }
                }
            }
        });
    } catch (error) {
        console.error('Error rendering stock indices chart:', error);
    }
}

async function renderCommodityPricesChart() {
    try {
        const data = await fetchData('/api/commodity-prices');
        const labels = Object.keys(data);
        const prices = labels.map(symbol => data[symbol].price);
        
        const ctx = document.getElementById('commodityPricesChart').getContext('2d');
        if (window.commodityPricesChartInstance) {
            window.commodityPricesChartInstance.destroy();
        }
        window.commodityPricesChartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Commodity Prices',
                    data: prices,
                    backgroundColor: 'rgba(255, 206, 86, 0.7)'
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    } catch (error) {
        console.error('Error rendering commodity prices chart:', error);
    }
}

async function renderCryptoPricesChart() {
    try {
        const data = await fetchData('/api/crypto-prices');
        const labels = Object.keys(data);
        const prices = labels.map(symbol => data[symbol].price_inr);
        
        const ctx = document.getElementById('cryptoPricesChart').getContext('2d');
        if (window.cryptoPricesChartInstance) {
            window.cryptoPricesChartInstance.destroy();
        }
        window.cryptoPricesChartInstance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Cryptocurrency Prices (INR)',
                    data: prices,
                    borderColor: 'rgba(153, 102, 255, 1)',
                    fill: false,
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: false }
                }
            }
        });
    } catch (error) {
        console.error('Error rendering cryptocurrency prices chart:', error);
    }
}
