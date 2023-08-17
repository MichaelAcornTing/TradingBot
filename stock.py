class Stock:
    def __init__(self, companyName, tickerSymbol, buyPrice):
        self.__companyName = companyName
        self.__tickerSymbol = tickerSymbol
        self.__buyPrice = buyPrice
        self.__sellPrice = None 

    def getCompanyName(self):
        return self.__companyName
    
    def getTickerSymbol(self):
        return self.__tickerSymbol
    
    def getBuyPrice(self):
        return self.__buyPrice
    
    def getCurrentPrice():
        # API request to get current price
        pass 

    def setSellPrice(self, sellPrice):
        self.__sellPrice = sellPrice
    
    def getSellPrice(self):
        return self.__sellPrice
    
    
    