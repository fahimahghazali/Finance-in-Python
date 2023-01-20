# finance-in-python
stocktrader -- A Python module for virtual stock trading
## About
### Functions
- `normaliseDate(s)` converts date string s to YYYY-MM-DD for standardisation throughout the module
- `loadStock(symbol)` loads file symbol.csv into stocks dictionary in module.
- `loadPortfolio(fname='portfolio.csv')` empties any elements in both transactions list and portfolio dictionary in the module
    and loads the csv file fname to the portfolio dictionary.
- `valuatePortfolio(date = 'empty', verbose = False)` valuates capital (cash and symbol) in portfolio dictionary at the input date
    symbol in portfolio is valued using low values of stocks available in stocks dictionary
- `addTransaction(trans, verbose = False)` updates the values of the keys in the portfolio and the `trans` dictionary is also appended to transaction list in the module
- `savePortfolio(fname = "portfolio.csv")` saves the current portfolio dictionary to a csv file called `fname` into the same directory as the module.
- `sellAll(date = "empty", verbose = False)` sells all shares available in portfolio dictionary at the low daily price 
    listed in stocks and updates the values of the keys in the portfolio
- `loadAllStocks()` loads all stocks available in the directory into the dictionary stocks
- `tradeStrategy1(verbose)` applies a certain flow of strategy to the current portfolio
Note: further information on functions are available in the docstrings

### Defined iterables

The stocks dictionary: \
Dictionary contains historical financial data of shares represented as symbol, where the value is a dictionary for each symbol key. Stocks dictionary general format is as follows
    
    stocks = {symbol:
                  {date : [ Open, High, Low, Close ],
                   #...},
               symbol:
                   {date : [ Open, High, Low, Close ],
                    #...},
              #... 
              }
   where
   [ Open, High, Low, Close ] are a list of prices of stocks symbol on the paired date \
   High and Low is the range that the price takes as it changes in the day while \
   Open and Close is the opening and closing price the stock takes.

The portfolio dictionary:\
    When loaded, portfolio dictionary contains "date" of the portfolio, 
    "cash" in portfolio and "symbol" if there are any in said portfolio as the keys.
    Using the example input, if the portfolio is printed the output is as follows,
    
    portfolio = { 
        'date' : '2012-1-16',
        'cash' : 20000,
        'SKY' : 5.0 *optional*
        'EZJ' : 8.0 *optional*
        }
        
where the value paired with the symbols are the number of said shares
in the portfolio (aka volume)

The transactions list: \
    A list of dictionaries that has contains the keys: "date"; "symbol"; "volume" that represent
    a transaction of buying(positively valued volume) or selling(negatively valued volume) 
    made in the portfolio.
    A valid transactions list example:
        
        transactions = [ 
            { 'date' : '2013-08-11', 'symbol' : 'SKY', 'volume' : -5 }, 
            { 'date' : '2013-08-21', 'symbol' : 'EZJ', 'volume' : 10 } 
        ]
