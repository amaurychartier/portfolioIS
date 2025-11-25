
import pandas as pd
import yfinance as yf
from forex_python.converter import CurrencyRates

class Portfolio:
    def __init__(self, positions: pd.DataFrame):
        self.positions = positions
        self.data = {}
        self.fx = CurrencyRates()
        # Mapping des symboles pour Yahoo Finance
        self.symbol_map = {
            'MUV2': 'MUV2.F', 'MOUR': 'MOUR.BR', 'DG': 'DG.PA', 'VETN': 'VETN.SW',
            'NOVN': 'NOVN.SW', 'ENI': 'ENI.MI', 'IBE': 'IBE.MC', '5Y2': '5Y2.F',
            'BOL': 'BOL.PA', '7NX': '7NX.F', 'SHEL': 'SHEL.L'
        }

    def load_current_prices(self):
        for ticker in self.positions['Symbol']:
            try:
                ticker_yf = self.symbol_map.get(ticker, ticker)
                price = yf.Ticker(ticker_yf).history(period="1d")['Close'].iloc[-1]
                self.data[ticker] = price
            except Exception:
                self.data[ticker] = None

    def calculate_performance(self):
        results = []
        for _, row in self.positions.iterrows():
            ticker = row['Symbol']
            entry_price = float(str(row['Unit cost']).replace(',', '.'))
            qty = int(row['Quantity'])
            currency = row['Currency'].strip()

            # Taux de change en temps réel
            try:
                rate = self.fx.get_rate(currency, 'CHF')
            except:
                rate = 1.0

            current_price = self.data.get(ticker, None)

            if current_price:
                entry_price_chf = entry_price * rate
                current_price_chf = current_price * rate
                total_value_chf = current_price_chf * qty
                pl_chf = (current_price - entry_price) * qty * rate
                roi = ((current_price - entry_price) / entry_price) * 100
            else:
                entry_price_chf, current_price_chf, total_value_chf, pl_chf, roi = None, None, None, None, None

            results.append({
                'Ticker': ticker,
                'Entry Price': entry_price,
                'Current Price': current_price,
                'Quantity': qty,
                'Currency': currency,
                'Entry Price CHF': entry_price_chf,
                'Current Price CHF': current_price_chf,
                'Total Value CHF': total_value_chf,
                'P/L CHF': pl_chf,
                'ROI %': roi
            })

        return pd.DataFrame(results)
