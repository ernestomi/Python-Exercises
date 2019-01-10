#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Practice Exercises for Python
Knapsack
Ernesto Monroy

This file contains 2 samples of Knapsack Problems. Greedy Fractional, which 
takes in a list of available items with value and weight, takes in a function
to apply and optimise on, and simply tries to fit in as many items as possible
based on the function to optimise

The second sample uses player data from a fantasy football website as input and
creates a team with a fixed number of positions by optimising on a function. It
is the same algorithm as the first, but constrained to a set number of positions

"""

from bs4 import BeautifulSoup


##########################################
# Greedy fractional knapsack

def greedy_fractional(items, max_weight, key_function):
    """
    Greedy fractional knapsack solution

    Parameters:
        items - list of Items
        max_weight - knapsack size
        key_function - function to sort items with

    Returns:
        list with the highest-value set of items fitting the knapsack:
            each item of the list should be a tuple (item, fraction_of_item_in_knapsack)
        the value of the resulting knapsack
    Example use:
    >>> names = ['clock', 'painting', 'radio']
    >>> values = [175,90,20]
    >>> weights = [10,9,4]
    >>> items = [Item(n, v, w) for n,v,w in zip(names, values, weights)]
    >>> res, val = greedy_fractional(items, 5, density)
    >>> val
    87.5
    >>> res, val = greedy_fractional(items, 13, density)
    >>> val
    205.0
    >>> res, val = greedy_fractional(items, 11, weight_inverse)
    >>> val
    90.0
    """

    # Sort items
    sorted_items = sorted(items, key=key_function, reverse=True)
    result = []  # list of tuples: each item is (item, fraction of the item in knapsack), eg (item,0.8)
    total_value = 0.0  # knapsack value
    total_weight = 0.0  # knapsack weight <= max_weight

    # Loop through all items
    for i in range(len(sorted_items)):
        cur_item = sorted_items[i]
        # If we can fit item into knapsack, do it and update its weight and value
        if ((total_weight+cur_item.get_weight())<=max_weight):
            # if we can fit the entire item into knapsack, do it, update its weight and value
            # code: add item to knapsack
            result.append(cur_item)
            # code: update knapsack weight and value
            total_value +=   cur_item.get_value()
            total_weight += cur_item.get_weight()
        else:  # If cannot fit full item, fill knapsack to capacity
            result.append(cur_item)
            # code: update knapsack weight and value
            total_value += ((max_weight-total_weight)/cur_item.get_weight())*cur_item.get_value()
            total_weight = max_weight
    return result, total_value


##########################################
# Helper functions for greedy fractional

def value(item):
    """
    Return the value of the item

    Parameters:
        item - an Item object

    Returns:
        the value of the item
    """
    return item.get_value()


def weight_inverse(item):
    """
    Return the inverse of item weights

    Parameters:
        item - an Item object

    Returns:
        the inverse of the item's weight
    """
    return 1/item.get_weight()


def density(item):
    """
    Return the item's ratio of value to weight

    Parameters:
        item - an Item object

    Returns:
        the ratio of value to weight
    """
    return item.get_value() / item.get_weight()


##########################################
# Greedy heuristic with team constraints

def greedy_heuristic(items, max_weight, key_function):
    """
    Greedy knapsack solution with team constraints

    Parameters:
        items - list of Items
        max_weight - knapsack size
        key_function - function to sort items with

    Returns:
        list with the highest-value set of items fitting the knapsack
        the value of the resulting knapsack
    Example use:
    >>> html = 'Player List - Fantasy Premier League.html'
    >>> pl_items, players = read_players(html)
    >>> rs, v = greedy(pl_items, 900, density)
    >>> print(v)
    >>> for item in rs:
    >>>     print(item)
    
    """

    # max players for each position
    max_position =	{
                      "Goalkeeper": 1,
                      "Defender": 4,
                      "Midfielder": 4,
                      "Forward":2
                    }

    # init: sort items
    sorted_items = sorted(items, key=key_function, reverse=True)
    result = []
    
    total_value = 0.0  # knapsack value
    total_weight = 0.0  # knapsack weight <= max_weight
    total_headcount =	{
                  "Goalkeeper": 0,
                  "Defender": 0,
                  "Midfielder": 0,
                  "Forward":0
                }
    total_players=0
    
    # Loop through sorted items
    for index in range(len(sorted_items)):
        cur_item = sorted_items[index]  
        #Check we havent reached the MAX players (so we dont check pointlessly when we are full)
        if (total_players>=11):
            return result, total_value
        #Check we havent reached the max players for its kind
        elif (max_position[cur_item.get_position()]>total_headcount[cur_item.get_position()]):
            #Check we havent reached the max weight
            if ((total_weight+cur_item.get_weight())<=max_weight):
                # if we can fit the entire item into knapsack, do it, update its weight and value
                # code: add item to knapsack
                result.append(cur_item)
                # code: update knapsack weight and value and position count
                total_value +=   cur_item.get_value()
                total_weight += cur_item.get_weight()
                total_headcount[cur_item.get_position()] += 1
                total_players += 1
    
    return result, total_value

###########################################
# Player class for greedy heuristics

class Player(object):
    """
    Player class for knapsack problem

    Has a name, a team, a value, and a weight, position.
    """
    def __init__(self, n, t, v, w, p):
        self.name = n
        self.team = t
        self.position = p
        self.value = int(v)
        self.weight = int(w)

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value

    def get_position(self):
        return self.position

    def get_weight(self):
        return self.weight

    def __str__(self):
        result = '<' + self.name + ', ' + self.position + ', ' + self.team + ', ' + str(self.value) \
                 + ', ' + str(self.weight) + '>'
        return result

    __repr__ = __str__ # nice representation of objects in eg lists


###########################################
# Helper functions for greedy heuristics


def create_player_list(players):
    """
    Create a list of player objects from list of player data lists
    """

    wages = [float(i[3][1:]) for i in players]
    pos = ['Goalkeeper', 'Defender', 'Midfielder', 'Forward']
    pos_index = 0
    # Hack to add correct position. Exploits the ordering on the website (position, wage). Very fragile!
    for i, pl in enumerate(players):
        if i > 0 and wages[i] > wages[i - 1]:
            pos_index += 1
        pl.append(pos[pos_index])

    # Create list of players. Convert wage to integer value.
    player_list = [Player(n, t, int(v), int(10 * float(w[1:])), p) for (n, t, v, w, p) in players]

    return player_list


def read_players(html):
    """
    Get player data from HTML file

    Assumes html is a webpage formatted like https://fantasy.premierleague.com/player-list/
    
    These are ordered by position and wage
    
    We could use the requests library to download the data:
    >>> import requests
    >>> r = requests.get('https://fantasy.premierleague.com/player-list/')
    >>> with open('test.html', 'w', encoding='utf-8') as f: 
    ...     data = f.write(r.text) # save html to file (only if we need it later, normally we would skip this)
    >>> read_players('test.html')
    """
    with open(html, 'r', encoding='utf-8') as f:
        data = f.read()
    soup = BeautifulSoup(data, 'lxml')

    # Read HTML table with soup
    players = []
    for tr in soup.find_all('tr'):
        row = tr.find_all('td')
        if len(row) > 0:
            players.append([elem.text for elem in row])

    # Get players as list
    player_list = create_player_list(players)

    return player_list, players