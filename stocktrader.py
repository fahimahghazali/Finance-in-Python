"""
stocktrader -- A Python module for virtual stock trading

Functions
---------
    normaliseDate(s)
    loadStock(symbol)
    loadPortfolio(fname='portfolio.csv')
    valuatePortfolio(date = 'empty', verbose = False)
    addTransaction(trans, verbose = False)
    savePortfolio(fname = "portfolio.csv")
    sellAll(date = "empty", verbose = False)
    loadAllStocks()
    tradeStrategy1(verbose)

Defined terables
----------------
The stocks dictionary:
    dictionary contains historical financial data of shares represented as symbol, 
        where the value is a dictionary for each symbol key.
    stocks dictionary general format is as follows
    stocks = {symbol:
                  {date : [ Open, High, Low, Close ],
                   #...},
               symbol:
                   {date : [ Open, High, Low, Close ],
                    #...},
              #... 
              }
    where
    [ Open, High, Low, Close ] are a list of prices of stocks symbol on the paired date
    High and Low is the range that the price takes as it changes in the day while 
    Open and Close is the opening and closing price the stock takes.


The portfolio dictionary:    
    when loaded, portfolio dictionary contains "date" of the portfolio, 
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

The transactions list:
    A list of dictionaries that has contains the keys: "date"; "symbol"; "volume" that represent
    a transaction of buying(positively valued volume) or selling(negatively valued volume) 
    made in the portfolio.
    A valid transactions list example:
        transactions = [ 
            { 'date' : '2013-08-11', 'symbol' : 'SKY', 'volume' : -5 }, 
            { 'date' : '2013-08-21', 'symbol' : 'EZJ', 'volume' : 10 } 
        ]

Full name: Nurfahimah binti Mohd Ghazali
StudentId: 10499719
Email: nurfahimah.mohdghazali@student.manchester.ac.uk
"""
import os
import pandas as pd
from datetime import datetime
import csv
stocks = {}
portfolio = {}
transactions = [] 

class TransactionError(Exception):
    pass

class DateError(Exception):
    pass


# task 1
def normaliseDate(s): 
    """
    Converts date string s to YYYY-MM-DD for standardisation throughout the module
    note: function does not check if date string s exists

    Parameters
    ----------
    s : str
        accepted input formats: YYYY-MM-DD, YYYY/MM/DD and DD.MM.YYYY, 
        where DD and MM are integers with one or two digits and YYYY is a four-digit integer.

    Raises
    ------
    DateError
        raised due to user input date string s not as accepted input formats listed.

    Returns
    -------
    str
        YYYY-MM-DD
        
    """
    for c in "-/.":
        s = s.replace(c, "-")
    lists = s.split("-")
    for i in lists:
        if (len(i) > 2 and len(i)!=4) or (len(s)>10 and len(s)<8):
            raise DateError("input format not as YYYY-MM-DD, YYYY/MM/DD or DD.MM.YYYY")
        
        else:
            if len(i)==1:
                lists[lists.index(i)] = "0"+i
            rl = lists[:]
            for k in rl:
                if len([k for i in lists if i==k])==2:
                    return "".join(i for i in lists if len(i)==4) + "-" + \
                        "-".join(k for i in lists if i==k )
    return "".join(i for i in lists if len(i)==4) + "-" +\
        "".join(i for i in lists if len(i)<=2 and lists.index(i)==1) + "-" +\
            "".join(i for i in lists if len(i)<=2 and lists.index(i)!=1)

#task 2
def loadStock(symbol):
    """
    loads file symbol.csv into stocks dictionary in module.
    The csv file is in the format:
        - must contain columns with the following headers: Date;Open;High;Low;Close
        - date column in file will be standardised using normaliseDate(s) function,
          so it must be in the form of accepted inputs for s: YYYY-MM-DD, YYYY/MM/DD or DD.MM.YYYY              
    
    Parameters
    ----------
    symbol : str
        stock 'symbol' also called shares from file symbol.csv in working directory.

    Raises
    ------
    FileNotFoundError
        raised due to symbol.csv not being in the directory.
    
    ValueError
        raised due to DateError in normaliseDate(date) 
        which is when date input is not in the form of: YYYY-MM-DD, YYYY/MM/DD or DD.MM.YYYY.

    Returns
    -------
    None.

    """
    try:
        f = pd.read_csv(symbol +".csv", sep=",", index_col=False, header = "infer", \
            usecols = ["Date", "Open", "High", "Low","Close"])
        dic = {}
        for i in range(f.shape[0]):
            dic[normaliseDate(f["Date"][i])] = [f["Open"][i],f["High"][i],f["Low"][i],f["Close"][i]]
        stocks[symbol] = dic
    except FileNotFoundError:
        raise 
    except DateError:
        raise ValueError("Date input in file not formatted as YYYY-MM-DD, YYYY/MM/DD or DD.MM.YYYY")
    except ValueError:
        raise

#task 3
def loadPortfolio(fname='portfolio.csv'):
    """
    empties any elements in both transactions list and portfolio dictionary in the module
    and loads the csv file fname to the portfolio dictionary. 
    
    Parameters
    ----------
    fname : str, optional
        The default is 'portfolio.csv'. general format:
            date
            cash
            symbol,volume  *optional*
            symbol,volume  *optional*
            #...
        
        date in the file must be in the format that is accepted by normaliseDate(s) function
        example of accepted csv file:
            2012/1/16
            20000
            SKY,5
            EZJ,8

    Raises
    ------
    FileNotFoundError
        raised due to fname file not being in the directory.
    
    ValueError
        raised when portfolio is not of the general format 
        or date is not one of the accepted formats: YYYY-MM-DD, YYYY/MM/DD or DD.MM.YYYY

    Returns
    -------
    None.

    """
    portfolio.clear()
    transactions.clear()
    try:
        f = pd.read_csv(fname, sep=",", index_col=False, header = None, names = range(2))
        portfolio["date"] = normaliseDate(f.iloc[0][0])
        portfolio["cash"] = f.iloc[1][0]
        for i in range(2, f.shape[0]):
            portfolio[f.iloc[i][0]] = f.iloc[i][1]
        if pd.isna(f.iloc[0][1]) == False and pd.isna(f.iloc[1][1]) == False:
            raise ValueError("portfolio file is in incorrect format")
    
    except FileNotFoundError:
        raise
    except DateError:
        raise ValueError("Date input in file not formatted as YYYY-MM-DD, YYYY/MM/DD or DD.MM.YYYY")
         
#task 4
def valuatePortfolio(date = 'portfolio date', verbose = False):
    """
    function valuates capital (cash and symbol) in portfolio dictionary at the input date
    symbol in portfolio is valued using low values of stocks available in stocks dictionary

    Parameters
    ----------
    date : str, optional
        The default is 'portfolio date'- date will take portfolio date by default
        Must be in one of the formats: YYYY-MM-DD, YYYY/MM/DD or DD.MM.YYYY to be 
        standardised using normaliseDate(s)
    
    verbose : boolean, optional
        The default is False.
        When False, function only returns totval.
        When True, funtion returns totval 
            as well as print the date of valuation and 
            a table detailing the values added that make up the valuation 
            which include the following ordered columns:
                1. capital type: cash and stock symbols
                2. the volume of cash and stock symbols in portfolio
                3. value per unit of stock symbols
                4. total value of each symbol in portfolio
            and in the final row of the final column is the total value of portfolio.   

    Raises
    ------
    DateError
        raised when date is not included in the dates key of the symbol dictionary in stocks
        or when the input date if earlier than the portfolio's date.

    Returns
    -------
    totval : float
        total value of the portfolio at the date input

    """
    if date == 'portfolio date':
        date = portfolio["date"]
    ndatei = normaliseDate(date)
    if datetime.strptime(ndatei,"%Y-%m-%d") >= datetime.strptime(portfolio["date"],"%Y-%m-%d"):
        samekey =[]
        for key in portfolio.keys():
            samekey.extend(key for i in stocks.keys() if key==i)
        totval = float(portfolio["cash"])
        for i in samekey:
            if ndatei not in stocks[i]:
                raise DateError("valuation date not on trading day")
            else:
                totval += float(portfolio[i])*float(stocks[i][ndatei][2]) 
        if verbose == False :
            return totval
        if verbose == True:
            print("Your portfolio on " + ndatei + ":"\
              "\n[* share values based on the lowest price on " +ndatei +"]"\
                  "\n\n Capital type          | Volume | Val/Unit* | Value in £*"\
                      "\n" +"-"*23 + "+" +"-"*8 + "+" +"-"*11 + "+" +"-"*13  +\
                          "\n {:<22}|{:>7} |{:>10.2f} |{:>12.2f} "\
                              .format("Cash","1", float(portfolio["cash"]), \
                                      float(portfolio["cash"])) )
            
            for i in samekey:
                args = ["Shares of " + i, portfolio[i], float(stocks[i][ndatei][2]), \
                        float(portfolio[i])*float(stocks[i][ndatei][2])]
                print(" {:<22}|{:>7.0f} |{:>10.2f} |{:>12.2f} ".format(*args))
                
            print("-"*23 + "+" +"-"*8 + "+" +"-"*11 + "+" +"-"*13 +\
              "\n {:<43} {:>12.2f}".format("TOTAL VALUE", totval))
            return totval
    if datetime.strptime(ndatei,"%Y-%m-%d") < datetime.strptime(portfolio["date"],"%Y-%m-%d"):
        raise DateError("valuation date earlier than portfolio date")

#task 5     
def addTransaction(trans, verbose = False):
    """
    The function updates the values of the keys in the portfolio:
        - changes date of portfolio to transcation date in trans
        - updates the volume of share symbol in portfolio after transcation,
            decreases the volume if shares are sold, *sold at low price in stocks*,
            increases the volume if shares are bought *bought at high price in stocks*,
            the share symbol is deleted if all are sold, and
            the share symbol is inserted if not already in portfolio when bought
        - updates the amount of cash in portfolio after transaction
    the dictionary trans is also appended to transaction list in the module
    
    Parameters
    ----------
    trans : dictionary
        Must be in the general format:
            trans = {"date": transaction date, "symbol": share to transact, "volume": volume}
            where transaction date is a string in one of the following formats: 
                YYYY-MM-DD, YYYY/MM/DD or DD.MM.YYYY
            symbol is any symbol in stocks if volume is positive-valued, 
                which means that the symbol is being bought
            and if volume is positive-valued, symbol must be a key in the portfolio dictionary
                where said symbol is being sold.
        example of accepted format:
            { 'date' : '2013-08-12', 'symbol' : 'SKY', 'volume' : -5 }
    verbose : boolean, optional
        The default is False.
        If False, function only updates portfolio and transactions list
        If True, function does updates as well as 
        print a summary of transaction and the remaining or available cash in portfolio
    
    Raises
    ------
    DateError
        raised due to transaction date in trans earlier that the portfolio date.
    ValueError
        raised due to symbol value in trans not in stocks dictionary.
    TransactionError
        raised due to if there are not enough volume of shares in portfolio to be sold.
            ie volume in trans -5 but volume of shares available in portfolio is 4
        or due to volume of symbol in trans is negative but said symbol is not included in portfolio
            ie no shares to sell

    Returns
    -------
    None.

    """
    ndate = normaliseDate(trans["date"])
    if datetime.strptime(ndate,"%Y-%m-%d") < datetime.strptime(portfolio["date"],"%Y-%m-%d"):
        raise DateError("transaction date earlier than portfolio date")
    if trans["symbol"] not in stocks.keys():
        raise ValueError("symbol value of the transaction is not listed in the stocks dictionary,")
    portfolio["date"] = ndate
    pcb = portfolio["cash"]
    if trans["symbol"] in portfolio:
        civ = float(portfolio[trans["symbol"]]) + float(trans["volume"])
        if civ == 0: 
            del portfolio[trans["symbol"]]
        if civ < 0 :
            raise TransactionError("not enough shares in portfolio to sell")
        if civ > 0:
            portfolio[trans["symbol"]] = civ
        
        if trans["volume"] < 0:
            portfolio["cash"] = float(pcb) - float(trans["volume"])*float(stocks[trans["symbol"]][ndate][2]) 
        if trans["volume"] > 0:
            portfolio["cash"] = float(pcb) - float(trans["volume"])*float(stocks[trans["symbol"]][ndate][1])
        if portfolio["cash"] <0:
            raise TransactionError("not enough capital to complete transaction")
    else:
        if trans["volume"] < 0:
            raise TransactionError("no shares to sell to complete transaction")
        portfolio[trans["symbol"]] = trans["volume"]
        portfolio["cash"] = float(pcb) - float(trans["volume"])*float(stocks[trans["symbol"]][ndate][1])
    transactions.append(trans.copy())
    if verbose == True:
        if trans["volume"] < 0:
            print("> {}: Sold {:.0f} shares of {} for a total of {:.2f} \nAvailable cash: {:.2f}"\
                  .format(ndate, -float(trans["volume"]), trans["symbol"], float(portfolio["cash"]) - float(pcb), float(portfolio["cash"]) ))
        if trans["volume"] > 0:
            print("> {}: Bought {:.0f} shares of {} for a total of {:.2f} \nRemaining cash: {:.2f}"\
                  .format(ndate, float(trans["volume"]), trans["symbol"], float(pcb) - float(portfolio["cash"]) , float(portfolio["cash"] )))
    else:
        pass

#task 6
def savePortfolio(fname = "portfolio.csv"):
    """
    saves the current portfolio dictionary to a csv file called fname into the same directory as the module.
    The file will be in the following general format:
            date
            cash
            symbol,volume  
            symbol,volume
            #...
    and can be loaded into a console using the loadPortfolio(fname) function. 
       
    Parameters
    ----------
    fname : str, optional
        must include ".csv" in the variable. The default is "portfolio.csv".

    Returns
    -------
    None.

    """
    newpfopen = open(fname, "wt")
    newpfopen.truncate()
    newp = csv.writer(newpfopen)
    for key, value in portfolio.items():
        if key == "date" or key =="cash":
            newp.writerow([value])
        else:
            newp.writerow([key, value])
    newpfopen.close()  
      
#task 7
def sellAll(date = "portfolio date", verbose = False):
    """
    The function sells all shares available in portfolio dictionary at the low daily price 
    listed n stocks.
    The function updates the values of the keys in the portfolio:
        - changes date of portfolio to date argument
        - all share symbols is deleted 
        - updates the amount of cash in portfolio after transactions
    
    Each selling transaction dictionary is also appended to transaction list in the module
    where dictionary is of the format:
        trans = {"date": transaction date, "symbol": share to transact, "volume": volume}
        
    Parameters
    ----------
    date : str, optional
        The default is "portfolio date" - date will take portfolio date by default
        Must be in one of the formats for user-input : YYYY-MM-DD, YYYY/MM/DD or DD.MM.YYYY
    
    verbose : boolean, optional
        The default is False.
        If False, function updates portfolio dictionary and transactions list.
        If True, fuction does updates as listed and 
        prints summary of transaction for each share in portfolio.

    Returns
    -------
    None.

    """
    if date == "portfolio date":
        date = portfolio["date"]
    ndate = normaliseDate(date)  
    keycopy = portfolio.copy()
    for key in keycopy.keys():
        if key != "date" and key !="cash":
            trans = {"date": ndate, "symbol": key, "volume": -portfolio[key]}
            addTransaction(trans, verbose)

#task 8
def loadAllStocks():   
    """
    Function loads all stocks available in the directory into the dictionary stocks.
    The csv file accepted is in the format:
        - must contain columns with the following headers: Date;Open;High;Low;Close
        - date column in file will be standardised using normaliseDate(s) function,
          so it must be in the form of accepted inputs for s: YYYY-MM-DD, YYYY/MM/DD or DD.MM.YYYY              
    
    Any files in the directory that do not meet the requirements will be ignored.
    
    Returns
    -------
    None.

    """
    path = os. getcwd()
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    csvf = [f[:-4] for f in files if ".csv" in f]
    for f in csvf:
        try:
            loadStock(f)
        except ValueError:
            pass
        
#task 9
def tradeStrategy1(verbose):
    """
    Function applies the following flow of strategy to the current portfolio
    - portfolio is updated according to the date, the available cash and 
      the volume of share held after every transaction
    - each transaction dictionary is appended to transactions list where the dictionary is of the form:
        trans = {"date": transaction date, "symbol": share to transact, "volume": volume}
    
    Flow of strategy
    ----------------
    1. Earliest buying date:
        The tenth trading day in stocks dictionary or 
        the date of portfolio if it is later than the tenth day.
        
    2. Which to buy
        
        qbuy = (10 times of the highest price of share in stocks on current trading day)
            /(sum of highest prices of previous 9 trading days and of current trading day*)
        
        qbuy is calculated for each share in stocks
            the share that has the maximum value for qbuy is chosen to buy
            if two or more shares are maximum, choose the first in lexicological order
        NOTE: only ONE share will be held until it is sold
        
    3. Buy shares    
        maximum volume of shares possible to be bought with available cash
        NOTE: if available cash is less than the value of 1 share chosen to be bought
              go back to step 2 for the next trading date.
              
    4. When to sell 
        
        qsell = (lowest price of share on trading dates after share is bought)
            /(highest price of share in stocks on trading day the share is bought) 
            
        qsell is calculated for each trading day after share is bought
            if qsell < 0.7 or qsell > 1.3, 
            meaning that the share has caused more than 30% loss 
            or more than 30% profit respectively
            
    5. On the next trading date, 
        repeat steps 2 - 5 until all available trading dates in stocks dictionary 
        are gone through        

    
    Parameters
    ----------
    verbose : boolean
        If False, the portfolio dictionary and transcations list is updated 
        according to the strategy   
    
        If True, the portfolio dictionary and transcations list is updated 
        according to the strategy and the function prints out the summary of 
        each transaction made in the trade strategy.

    Returns
    -------
    None.

    """
    tradingdates = list(stocks[list(stocks.keys())[0]].keys())
    if datetime.strptime(portfolio["date"],"%Y-%m-%d") > datetime.strptime(tradingdates[9],"%Y-%m-%d"):
        j1 = portfolio["date"]
    else:
        j1 = tradingdates[9]
    try:    
        while j1 in tradingdates:
            tradingdates = list(stocks[list(stocks.keys())[0]].keys())       
            trad10db = tradingdates[( tradingdates.index(j1) + 1 -10) : (tradingdates.index(j1) + 1)]        
            tradhp10b = []        
            qbuy = {}
            lst = list(stocks.keys())
            lst.sort()
            for key in lst:   
                for i in trad10db:
                    tradhp10b.append(float(stocks[key][i][1]))
                qbuy[key] = 10*float(stocks[key][j1][1]) / sum(tradhp10b) 
                tradhp10b.clear()        

            maxqbuy = "".join(key for key, value in qbuy.items() if value == max([qbuy[key] for key in qbuy.keys()]))
            maxcanbuy = 0
            maxvol = 0
            if float(portfolio["cash"]) < float(stocks[maxqbuy][j1][1]) :
                j1 = next(i for i in tradingdates if datetime.strptime(j1,"%Y-%m-%d")<datetime.strptime(i,"%Y-%m-%d")) 
                continue
        
            while (float(portfolio["cash"]) - maxcanbuy) > float(stocks[maxqbuy][j1][1]):
                maxcanbuy += float(stocks[maxqbuy][j1][1])
                maxvol += 1     
         
            trans = {"date" : j1, "symbol": maxqbuy, "volume" : maxvol}   
            addTransaction(trans, verbose = True)        

            qsell = {}
            for i in tradingdates[(tradingdates.index(j1) + 1):]:
                qsellc = float(stocks[maxqbuy][i][2])/float(stocks[maxqbuy][j1][1])
                qsell[i] = qsellc
            datetosell = next(key for key,value in qsell.items() if value < 0.7 or value > 1.3)
            sellAll(date = datetosell, verbose = verbose)       
            j1 = next(i for i in tradingdates if datetime.strptime(datetosell,"%Y-%m-%d")<datetime.strptime(i,"%Y-%m-%d"))  
    except  StopIteration:
        pass
            

















        
        