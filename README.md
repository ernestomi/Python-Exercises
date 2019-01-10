# Python Exercises

Hi there! This repo is dedicated to some exercises I did whilst learning Python. You will find all the files in exercises folder.

## The Knapsack
This is a classic optimisation problem, where we have a constraint (e.g. the size of a bag) and items with a value that we want to optimise (e.g. gear to carry). There are many ways of solving a Knapsack problem, in this case, I have simply sorted all items available by a specific function that I am interested in optimising.

I also give a specific use case where I use footbal player data from a fantasy football website and try to create the best team by constraining the number of positions I have in the team (i.e. 1 goalkeeper, 3 attackers ...)

Wikipedia info for Knapsack: https://en.wikipedia.org/wiki/Knapsack_problem

## Network
This is a very simple analysis of a network represented with a graph of connected nodes, for simplicity. I have used a single direction graph, with no weight on the connections or the nodes. 

Here I present 2 methods for searching: the breath first which prioritises looking at the children of the node first before looking at the children's children, and the depth first which prioritises exploring each branch to its maximum depth first.

I also provide a practical example where I take movie data and look for the actor that is most distantly related to Kevin Bacon. In this case, actors are related by movies where they have acted together.

Wikipedia info for Depth First Search: https://en.wikipedia.org/wiki/Depth-first_search
Wikipedia info for Breadth First Search: https://en.wikipedia.org/wiki/Breadth-first_search

## Palindrome
This is an example of analysing a word by breaking it into characters. In here I take a number, and given a set number of changes allowed, I change the digits to try and make the largest palindrome possible

## Trading
In here I take a classic example of algorithmic trading. The concept I took was that of "Moving Average Crossovers", which indicates that when a short term moving average crosses above a long term moving average, it is the sign of a bullish market and you should buy. In the reverse case, the market is bearish and you should sell

Wikipedia info for MA Crossovers: https://en.wikipedia.org/wiki/Moving_average_crossover

Of course if there is a typo or suggestion to improve let me know! Or contact me for questions :)
