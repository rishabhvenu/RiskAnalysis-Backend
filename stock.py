import yfinance as yf
import web_scrape

class Stock:
    def __init__(self, ticker):
        self.ticker = yf.Ticker(ticker)

    def get_market_cap(self):
        outstanding_shares = self.ticker.get_shares_full().values[-1]
        share_price = self.ticker.history(period="1d").Close[0]
        market_cap = outstanding_shares * share_price
        return market_cap

    def get_beta(self):
        stock_history = self.ticker.history(period="5y").Close.tolist()
        spy_history = yf.Ticker("^GSPC").history(period="5y").Close.tolist()
        # If the stock length is below the length of SPY h
        if len(stock_history) < len(spy_history):
            del spy_history[:len(spy_history) - len(stock_history)]

        stock_returns = []
        spy_returns = []
        stock_return_total = 0
        spy_return_total = 0
        
        for i in range(1, len(stock_history)):
            current_day_close_stock = stock_history[i]
            previous_day_close_stock = stock_history[i - 1]
            stock_return = (current_day_close_stock - previous_day_close_stock) / previous_day_close_stock
            stock_return_total += stock_return
            stock_returns.append(stock_return)
            current_day_close_spy = spy_history[i]
            previous_day_close_spy = spy_history[i - 1]
            spy_return = (current_day_close_spy - previous_day_close_spy) / previous_day_close_spy
            spy_return_total += spy_return
            spy_returns.append(spy_return)

        stock_return_mean = stock_return_total / (len(stock_history) - 1)
        spy_return_mean = spy_return_total / (len(stock_history) - 1)
        covariance = 0

        for i in range(0, len(stock_returns)):
            covariance += (stock_returns[i] - stock_return_mean) * (spy_returns[i] - spy_return_mean)

        covariance /= len(stock_returns) - 1

        variance = 0

        for spy_return in spy_returns:
            variance += (spy_return - spy_return_mean) ** 2

        variance /= len(spy_returns) - 1

        beta = covariance / variance
        return covariance, variance, beta

    def get_debt_to_equity(self):
        symbol = self.ticker.info["symbol"]
        total_debt = web_scrape.get_total_debt(symbol)
        shareholders_equity = web_scrape.get_shareholders_equity(symbol)
        total_debt_to_equity_ratio = total_debt / shareholders_equity
        return total_debt_to_equity_ratio

    def get_interest_coverage(self):
        symbol = self.ticker.info["symbol"]
        EBIT = web_scrape.get_EBIT(symbol)
        interest_expense = web_scrape.get_interest_expense(symbol)
        interest_coverage_ratio = EBIT / interest_expense
        return interest_coverage_ratio
