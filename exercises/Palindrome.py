#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Practice Exercises for Python
String Manipulation on a Palindrome
Ernesto Monroy

"""

def palindrome(s, k):
    """
    Find highest value palindrome from s with max k digit changes.
    
    Parameters:
        s - an integer in string format
        k - number of changes
        
    Returns:
        highest-value palindrome number in string format; 
        if creating a palindrome is not possible, returns the string 'Not possible.'
    
    Example use:
    >>> palindrome('1921', 2)
    '1991'
    >>> palindrome('1921', 3)
    '9999'
    >>> palindrome('11122', 1)
    'Not possible.'
    >>> palindrome('11119111', 4)
    '91199119'
    """
    # Your code here.
    
    #Counter
    spareMoves=k
    #Loop to find how many spare moves we got (to meet minimum)
    for i in range(0, round(len(s)/2)):
        if s[i]!=s[-i-1]:
            spareMoves+=-1
    
    #If not enough changes available alert
    if spareMoves<0:
        return 'Not possible.'
    
    #Convert string to list so we can easily replace
    stringList=list(map(int,list(s)))

    #Loop to execute changes
    for i in range(0, round(len(stringList)/2)):  
        #If I can optimize and have enough changes then change one to 9 (the other one is changed in the next if
        #(For equal numbers we need 2 spare moves since we didnt account for changing in the minumum moves)
        if max(stringList[i],stringList[-i-1])<9 and spareMoves>=(1+int(stringList[i]==stringList[-i-1])):
            #Remove the spares utilized
            spareMoves+=-(1+int(stringList[i]==stringList[-i-1]))
            #Change one side to 9 (the other side is changed in next if)
            stringList[i]=9

        #If there they are different, change one to match the other
        if stringList[i]!=stringList[-i-1]:
            stringList[i]=max(stringList[i],stringList[-i-1])
            stringList[-i-1]=stringList[i]
    
    #If there is an odd middle number and it can be optimized (no need to check for max(i,-i) since we are no longer wasting moves)
    if (len(s)%2==1 and spareMoves>0):
        stringList[round(len(s)/2)]=9
    
    return "".join(map(str,stringList))        