// Chart.js implementation for financial dashboard

class FinancialCharts {
    constructor() {
        this.charts = {};
        this.chartColors = {
            primary: '#0d6efd',
            success: '#198754',
            danger: '#dc3545',
            warning: '#ffc107',
            info: '#0dcaf0',
            light: '#f8f9fa',
            dark: '#212529'
        };
        
        this.init();
    }
    
    init() {
        Chart.defaults.font.family = 'system-ui, -apple-system, sans-serif';
        Chart.defaults.font.size = 12;
        
        // Set default colors based on theme
        const isDark = document.documentElement.getAttribute('data-bs-theme') === 'dark';
        Chart.defaults.color = isDark ? '#ffffff' : '#212529';
        Chart.defaults.borderColor = isDark ? '#495057' : '#dee2e6';
        Chart.defaults.backgroundColor = isDark ? '#212529' : '#ffffff';
    }
    
    createCurrencyChart(containerId, data) {
        const ctx = document.getElementById(containerId);
        if (!ctx) return;
        
        const chartData = {
            labels: Object.keys(data),
            datasets: [{
                label: 'Exchange Rate (INR)',
                data: Object.values(data).map(rate => rate.rate),
                backgroundColor: this.chartColors.primary,
                borderColor: this.chartColors.primary,
                borderWidth: 2,
                fill: false
            }]
        };
        
        const config = {
            type: 'bar',
            data: chartData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Currency Exchange Rates'
                    },
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        title: {
                            display: true,
                            text: 'Rate (INR)'
                        }
                    }
                }
            }
        };
        
        if (this.charts[containerId]) {
            this.charts[containerId].destroy();
        }
        
        this.charts[containerId] = new Chart(ctx, config);
    }
    
    createStockChart(containerId, data) {
        const ctx = document.getElementById(containerId);
        if (!ctx) return;
        
        const chartData = {
            labels: Object.values(data).map(stock => stock.name),
            datasets: [{
                label: 'Index Value',
                data: Object.values(data).map(stock => stock.value),
                backgroundColor: Object.values(data).map(stock => 
                    stock.change_percent >= 0 ? this.chartColors.success : this.chartColors.danger
                ),
                borderColor: Object.values(data).map(stock => 
                    stock.change_percent >= 0 ? this.chartColors.success : this.chartColors.danger
                ),
                borderWidth: 2
            }]
        };
        
        const config = {
            type: 'bar',
            data: chartData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Stock Indices Performance'
                    },
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        title: {
                            display: true,
                            text: 'Index Value'
                        }
                    }
                }
            }
        };
        
        if (this.charts[containerId]) {
            this.charts[containerId].destroy();
        }
        
        this.charts[containerId] = new Chart(ctx, config);
    }
    
    createCommodityChart(containerId, data) {
        const ctx = document.getElementById(containerId);
        if (!ctx) return;
        
        const chartData = {
            labels: Object.values(data).map(commodity => commodity.name),
            datasets: [{
                label: 'Price (INR)',
                data: Object.values(data).map(commodity => commodity.price),
                backgroundColor: [
                    this.chartColors.warning,
                    this.chartColors.info,
                    this.chartColors.dark
                ],
                borderColor: [
                    this.chartColors.warning,
                    this.chartColors.info,
                    this.chartColors.dark
                ],
                borderWidth: 2
            }]
        };
        
        const config = {
            type: 'doughnut',
            data: chartData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Commodity Prices'
                    },
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        };
        
        if (this.charts[containerId]) {
            this.charts[containerId].destroy();
        }
        
        this.charts[containerId] = new Chart(ctx, config);
    }
    
    createCryptoChart(containerId, data) {
        const ctx = document.getElementById(containerId);
        if (!ctx) return;
        
        const cryptoData = Object.values(data).slice(0, 6); // Top 6 cryptos
        
        const chartData = {
            labels: cryptoData.map(crypto => crypto.name),
            datasets: [{
                label: 'Price (INR)',
                data: cryptoData.map(crypto => crypto.price_inr),
                backgroundColor: cryptoData.map(crypto => 
                    crypto.change_percent >= 0 ? this.chartColors.success : this.chartColors.danger
                ),
                borderColor: cryptoData.map(crypto => 
                    crypto.change_percent >= 0 ? this.chartColors.success : this.chartColors.danger
                ),
                borderWidth: 2
            }]
        };
        
        const config = {
            type: 'horizontalBar',
            data: chartData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Cryptocurrency Prices'
                    },
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        beginAtZero: false,
                        title: {
                            display: true,
                            text: 'Price (INR)'
                        }
                    }
                }
            }
        };
        
        if (this.charts[containerId]) {
            this.charts[containerId].destroy();
        }
        
        this.charts[containerId] = new Chart(ctx, config);
    }
    
    createTrendChart(containerId, data, title) {
        const ctx = document.getElementById(containerId);
        if (!ctx) return;
        
        const chartData = {
            labels: data.map(item => item.time),
            datasets: [{
                label: title,
                data: data.map(item => item.value),
                backgroundColor: 'rgba(13, 110, 253, 0.1)',
                borderColor: this.chartColors.primary,
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        };
        
        const config = {
            type: 'line',
            data: chartData,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: title
                    },
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        title: {
                            display: true,
                            text: 'Value'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Time'
                        }
                    }
                }
            }
        };
        
        if (this.charts[containerId]) {
            this.charts[containerId].destroy();
        }
        
        this.charts[containerId] = new Chart(ctx, config);
    }
    
    updateChartTheme() {
        const isDark = document.documentElement.getAttribute('data-bs-theme') === 'dark';
        Chart.defaults.color = isDark ? '#ffffff' : '#212529';
        Chart.defaults.borderColor = isDark ? '#495057' : '#dee2e6';
        Chart.defaults.backgroundColor = isDark ? '#212529' : '#ffffff';
        
        // Update all existing charts
        Object.values(this.charts).forEach(chart => {
            chart.update();
        });
    }
    
    destroyChart(containerId) {
        if (this.charts[containerId]) {
            this.charts[containerId].destroy();
            delete this.charts[containerId];
        }
    }
    
    destroyAllCharts() {
        Object.keys(this.charts).forEach(chartId => {
            this.destroyChart(chartId);
        });
    }
}

// Initialize charts when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.financialCharts = new FinancialCharts();
    
    // Update chart theme when theme changes
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            setTimeout(() => {
                window.financialCharts.updateChartTheme();
            }, 100);
        });
    }
});

// Global chart functions
function createCurrencyChart(containerId, data) {
    window.financialCharts.createCurrencyChart(containerId, data);
}

function createStockChart(containerId, data) {
    window.financialCharts.createStockChart(containerId, data);
}

function createCommodityChart(containerId, data) {
    window.financialCharts.createCommodityChart(containerId, data);
}

function createCryptoChart(containerId, data) {
    window.financialCharts.createCryptoChart(containerId, data);
}

function createTrendChart(containerId, data, title) {
    window.financialCharts.createTrendChart(containerId, data, title);
}
