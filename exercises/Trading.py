#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Practice Exercises for Python
Trading Simulation
Ernesto Monroy

This simple functions use the trading technical analysis concept of simple 
moving averages. The theory is that when a short term moving average, crosees
above a long term moving average, its a sign of a bullish market, therefore 
signaling a buy, and vicecersa.

Here three functions calculate the moving average, the crossovers and a 
simulation of trading

"""

def moving_average(prices, n):
    """
    Calculates n-period moving average of a list of floats/integers.

    Parameters:
        prices: list of values (ordered in time),
        n: integer moving-average parameter

    Returns:
        list with None for the first n-1 values in prices and the appropriate moving average for the rest

    Example use:
    >>> ma = moving_average([2,3,4,5,8,5,4,3,2,1], 3)
    >>> [round(m, 2) if m is not None else None for m in ma]
    [None, None, 3.0, 4.0, 5.67, 6.0, 5.67, 4.0, 3.0, 2.0]
    >>> moving_average([2,3,4,5,8,5,4,3,2,1], 2)
    [None, 2.5, 3.5, 4.5, 6.5, 6.5, 4.5, 3.5, 2.5, 1.5]
    """
    # Your code here. Don't change anything above.
    #Avoid trying to calculate over a larger than possible range
    n=min(n,len(prices))
    #Pad to the left with None
    result=[None]*(n-1)
    #Iterate and calculate over the n range moving forward
    for i in range(0,len(prices)-n+1):
        result.append(sum(prices[i:i+n]) / n)
    return result

def cross_overs(prices1, prices2):
    """ 
    Identify cross-over indices for two equal-length lists of prices (here: moving averages)

    Parameters:
        prices1, prices2: lists of prices (ordered by time)

    Returns:
        list of crossover points

    Each item in the returned list is a list [time_index, higher_index], where:
        - time_index is the crossover time index (when it happends
        - higher_index indicates which price becomes higher at timeIndex: either 1 for first list or 2 for second list
    
    There are no crossovers before both price lists have values that are not None.
    You can start making comparisons from the point at which both have number values.
    
    Example use:
    >>> p1 = [1, 2, 4, 5]
    >>> p2 = [0, 2.5, 5, 3]
    >>> cross_overs(p1, p2)
    [[1, 2], [3, 1]]
    >>> p1 = [None, 2.5, 3.5, 4.5, 4.5, 3.5, 2.5, 1.5, 3.5, 3.5]
    >>> p2 = [None, None, 3.0, 4.0, 4.333333333333333, 4.0, 3.0, 2.0, 3.0, 2.6666666666666665]
    >>> cross_overs(p1, p2)
    [[5, 2], [8, 1]]
    """
    # Your code here. Don't change anything above.
    #Throw error if the lists are different!
    if len(prices1)!=len(prices2):
        raise ValueError('The given lists are not the same size')
    
    result=[]
    #Loop through the lists
    for i in range(1, len(prices1)):
        #If nones then ignore
        if prices1[i-1]!=None and prices2[i-1]!=None:
            #Calculate current and previous high (0 for equal)
            currentHigh=(int(prices1[i]!=prices2[i])+int(prices1[i]<prices2[i]))
            previousHigh=(int(prices1[i-1]!=prices2[i-1])+int(prices1[i-1]<prices2[i-1]))
            #If there is a crossover, add it (ignore when returning to equal since we only care when a price BECOMES strictly higher)
            if (currentHigh!=previousHigh and currentHigh!=0):
                result.append([i,currentHigh])
    
    return result
        
        
def make_trades(starting_cash, prices, crossovers):
    """
    Given an initial cash position, use a list of crossovers to make trades

    Parameters:
        starting_cash: initial cash position
        prices: list of prices (ordered by time)
        crossovers: list of crossover points on the prices

    Returns:
        list containing current value of trading position (either in stock value or cash) at each time index
    
    Assume each item crossovers[i] is a list [time_index, buy_index]
    Assume that buy_index = 1 means "buy"
    Assume that buy_index = 2 means "sell"

    We buy stock at any time_index where crossover's buy_index indicates 1, and sell at 2.
    In more detail:
        - We want to buy at time_index whenever buy_index = 1 and we currently hold a cash position
            - We buy at the stock price at time_index. We buy with the entire cash position we have and only hold stock
        - We want to sell at time_index when buy_index = 2 and we hold a stock position
            - We sell at the stock price at time_index. We sell our entire stock position and will only hold cash

    Whenever we trade, we buy with our entire cash position, or sell our entire stock position.
    We will therefore always hold either stock or cash, but never both.
    
    Assume we can hold fractional stock quantities, and there are no transaction fees.

    Example use:
    # In the first example, We start with cash 1.0.
    # We hold cash until we buy at index 1 at the price 4. We then hold 0.25 shares. 
    # After that, our portfolio is in stock, so its value fluctuates with the stock price.
    # As the stock price goes from 4 to 6, our portfolio value goes from 1.0 to 1.5.
    # This goes on until we sell at index 3 at the price 5. 
    # Then we hold cash again and the value of the portfolio does not change as it is in cash.
    >>> starting_cash = 1.0
    >>> prices = [2,4,6,5,1]
    >>> cos = [[1, 1], [3, 2]] # not real crossovers, just to illustrate portfolio value when trading
    >>> values = make_trades(starting_cash, prices, cos)
    >>> values 
    [1.0, 1.0, 1.5, 1.25, 1.25]
    >>> starting_cash = 1000.0
    >>> prices = [2,3,4,5,4,3,2,1,6,1,5,7,8,10,7,9]
    >>> cos = [[5, 2], [8, 1], [10, 2], [11, 1], [15, 2]]
    >>> values = make_trades(starting_cash, prices, cos)
    >>> [round(v, 2) for v in values] # round every value of the returned list using list comprehension
    [1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 166.67, 833.33, 833.33, 952.38, 1190.48, 833.33, 1071.43]
    >>> prices =[38,21,20,13,7,14,22,23,27,23,44,26,48,32,48,60,70,40,34,35,33]
    >>> crossovers = [[7, 1], [19, 2]]
    >>> money = 100.0
    >>> values = make_trades(money, prices, crossovers)
    >>> [round(v, 2) for v in values] # round every value of the returned list using list comprehension
    [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 117.39, 100.0, 191.3, 113.04, 208.7, 139.13, 208.7, 260.87, 304.35, 173.91, 147.83, 152.17, 152.17]
    """
    # Your code here. Don't change anything above.
    
    #Return initial cash if there is no crossovers
    if len(crossovers)<1:
        return [starting_cash]*len(prices)
    
    #Initialize with starting cash until first crossover
    current_value=[starting_cash]*(crossovers[0][0]+1)
    
    #Index for crossovers
    j=0
    
    #Loop all prices (after the first crossover)
    for i in range(crossovers[0][0]+1,len(prices)): 
        #Calculate next value (here abs(crossover) takes care of adding 0 when we have cash and 1 if we have stocks)
        current_value.append(current_value[-1]*(1+(prices[i]/prices[i-1]-1)*abs(crossovers[j][1]-2)))
        #If there is a next crossover and we already reached the crossover index jump to the next crossover
        if (j<(len(crossovers)-1) and i>=crossovers[j+1][0]):
            j+=1
    
    return current_value