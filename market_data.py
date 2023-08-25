import requests
import datetime
from api_endpoints import STOCK_PRICING_ENDPOINT

class MarketData:

    def __init__(self, KEY, SECRET_KEY):
        self.__HEADERS = {"APCA-API-KEY-ID": KEY, "APCA-API-SECRET-KEY": SECRET_KEY}


    def __get_current_price(self, ticker_symbol):
        # get latest trade data
        url = f"{STOCK_PRICING_ENDPOINT}/stocks/{ticker_symbol}/trades/latest"
        trade_response = requests.get(url, headers=self.__HEADERS)

        # check response error
        if(trade_response.status_code >= 400):
            error_message = trade_response.json()['message']
            raise Exception(f"Error ({trade_response.status_code}): {error_message}")
        else:
            trade_data = trade_response.json()
            return trade_data['trade']['p']
        
    def get_multiple_current_price(self, ticker_symbols):
        # get latest trade data
        url = f"{STOCK_PRICING_ENDPOINT}/stocks/trades/latest"
        parameters = {"symbols": ",".join(map(str, ticker_symbols))}
        trades_response = requests.get(url, headers=self.__HEADERS, params=parameters)

        # check response error
        if(trades_response.status_code >= 400):
            error_message = trades_response.json()['message']
            raise Exception(f"Error ({trades_response.status_code}): {error_message}")
        else:
            trades_data = trades_response.json()['trades']
            current_prices = {}
            for key, value in trades_data.items():
                current_prices[key] = value['p']
            print(f"Curent Prices: {current_prices}")
            return current_prices
        

    def __get_price_n_days_ago(self, ticker_symbol, n_days_ago):
        # get trade data n days ago
        start_time = self.__get_date_n_days_ago(n_days_ago)
        parameters = {"start": start_time, "limit": 1}
        url = f"{STOCK_PRICING_ENDPOINT}/stocks/{ticker_symbol}/trades"
        trade_response = requests.get(url, headers=self.__HEADERS, params=parameters)

        # check response error
        if(trade_response.status_code >= 400):
            error_message = trade_response.json()['message']
            raise Exception(f"Error ({trade_response.status_code}): {error_message}")
        else:
            trade_data = trade_response.json()
            trade_price = trade_data['trades'][0]['p']
            return trade_price
        
    
    def get_multiple_price_n_days_ago(self, ticker_symbols, n_days_ago):
        previous_prices = {}
        # get trade data n days ago
        for symbol in ticker_symbols:
            try:
                price = self.__get_price_n_days_ago(symbol, n_days_ago)
                previous_prices[symbol] = price
            except:
                previous_prices[symbol] = None
        print(f"Previous Prices: {previous_prices}")
        return previous_prices

    def __get_date_n_days_ago(self, n_days_ago):
        today = datetime.datetime.today()
        date = today - datetime.timedelta(days=n_days_ago)
        formatted_date = self.__get_formatted_date(date)
        return formatted_date
        

    def __get_formatted_date(self, date):
        base_time = "T08:00:00.00Z"
        formatted_date = date.strftime("%Y-%m-%d") + base_time
        return formatted_date

    def get_percentage_score_from_stock(self, ticker_symbol, n_days_ago):
        current_price = self.__get_current_price(ticker_symbol)
        previous_price = self.__get_price_n_days_ago(ticker_symbol, n_days_ago)
        return self.get_percentage_score(current_price, previous_price)
    
    def get_percentage_score(self, current_price, previous_price):
        percentage_score = ((current_price - previous_price) / previous_price) * 100
        return round(percentage_score, 2)
    
    def get_best_performing_stock_over_n_days(self, ticker_symbols, n_days_ago):
        best_stock = ticker_symbols[0]
        current_prices = self.get_multiple_current_price(ticker_symbols)
        previous_prices = self.get_multiple_price_n_days_ago(ticker_symbols, n_days_ago)
        scores = self.get_percentage_scores(current_prices, previous_prices)
        for stock, score in scores.items():
            if score > scores[best_stock]:
                best_stock = stock
        return best_stock
    
    def get_percentage_scores(self, current_prices, previous_prices):
        scores = {}
        for stock in current_prices:
            current_price = current_prices[stock]
            previous_price = previous_prices[stock]
            if current_price != None and previous_price != None:
                score = self.get_percentage_score(current_price, previous_price)
                scores[stock] = score
        print(f"Percentage Scores: {scores}")
        return scores
