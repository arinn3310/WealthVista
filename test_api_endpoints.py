import requests

BASE_URL = "http://127.0.0.1:5000/api"

endpoints = [
    "currency-rates",
    "stock-indices",
    "commodity-prices",
    "crypto-prices",
    "financial-news",
    "gainers-losers",
    "convert?from=USD&to=INR&amount=1"
]

def test_endpoints():
    for endpoint in endpoints:
        url = f"{BASE_URL}/{endpoint}"
        try:
            response = requests.get(url, timeout=10)
            print(f"GET {url} - Status: {response.status_code}")
            print(response.json())
        except Exception as e:
            print(f"Error testing {url}: {e}")

if __name__ == "__main__":
    test_endpoints()
