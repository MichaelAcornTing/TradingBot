import requests
import datetime
from api_endpoints import STOCK_PRICING_ENDPOINT

class MarketData:

    def __init__(self, KEY, SECRET_KEY):
        self.__HEADERS = {"APCA-API-KEY-ID": KEY, "APCA-API-SECRET-KEY": SECRET_KEY}


    def get_current_price(self, ticker_symbol):
        # get latest trade data
        url = f"{STOCK_PRICING_ENDPOINT}/stocks/{ticker_symbol}/trades/latest"
        trade_response = requests.get(url, headers=self.__HEADERS)

        # check response error
        if(trade_response.status_code >= 400):
            error_message = trade_response.json()['message']
            print(f"Error ({trade_response.status_code}): {error_message}")
        else:
            trade_data = trade_response.json()
            return trade_data['trade']['p']
        

    def get_price_n_days_ago(self, ticker_symbol, n_days_ago):
        # get trade data 2 days ago
        start_time = self.__get_date_n_days_ago(n_days_ago)
        parameters = {"start": start_time, "limit": 1}
        url = f"{STOCK_PRICING_ENDPOINT}/stocks/{ticker_symbol}/trades"
        trade_response = requests.get(url, headers=self.__HEADERS, params=parameters)

        # check response error
        if(trade_response.status_code >= 400):
            print(trade_response.text)
        else:
            trade_data = trade_response.json()
            trade_price = trade_data['trades'][0]['p']
            return trade_price

    def __get_date_n_days_ago(self, n_days_ago):
        today = datetime.datetime.today()
        date = today - datetime.timedelta(days=n_days_ago)
        formatted_date = self.__get_formatted_date(date)
        return formatted_date
        

    def __get_formatted_date(self, date):
        base_time = "T08:00:00.00Z"
        formatted_date = date.strftime("%Y-%m-%d") + base_time
        return formatted_date


    def get_percentage_score(self, current_price, previous_price):
        percentageScore = ((current_price - previous_price) / previous_price) * 100
        return round(percentageScore, 2)


