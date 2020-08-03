# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 11:02:00 2020

@author: Philipp


This program is supposed to find (via depth-first-search) a way of one knight
to visit all locations on a chess board exactly once.
"""

import time
import queue
import numpy as np
import functools

class KnightState:
    @functools.total_ordering
    # Creating a state:
    # currentLocation is a list [x,y], where x, y are the coordinates 
    #       of the knight
    # previousVisited is an 8x8 array with entries 0 and 1
    #       0 if the knight has not been there yet on his path
    #       1 if it has been there on his path
    
    def __init__(self, currentLocation, previousVisited = np.zeros([8,8], dtype=int), includeCurrent=False):
        self.currentLocation = currentLocation # depicts the current location of the knight
        self.previousVisited = previousVisited # Tracks which states have been visited previously 
        
        if includeCurrent:
        # set the current location as visited; only used for initialization
            self.previousVisited[currentLocation[0], currentLocation[1]] = 1
    
    # make the printing nice
    def __str__(self):
        return "({},{} ; {})".format(self.currentLocation[0], self.currentLocation[1], self.previousVisited.sum()-1)
    
    def __repr__(self):
        return self.__str__()
    
    # Get all successor states w.r.t. a legal knight move
    # returns list of KnightState instances
    def successors(self):
        successorList = [] # collect all successor states
        
        def checkVal(newX, newY): # checking the validity of the new potential state
            return newX <8 and newX>=0 and newY<8 and newY>=0 and self.previousVisited[newX, newY]==0
        
        # all potential knight moves:
        moveset = [ (+2,+1),(+2,-1),(-2,+1),(-2,-1),(-1,+2),(-1,-2),(+1,-2),(+1,+2)]
        
        # shuffle the moveset to encourage less repetetive patterns
        np.random.shuffle(moveset)
        for delX, delY in moveset:
            if checkVal(self.currentLocation[0]+delX, self.currentLocation[1]+delY):
                newVisit = np.zeros([8,8],dtype=int)
                newVisit[self.currentLocation[0]+delX, self.currentLocation[1]+delY] = 1
                successorList.append(KnightState([self.currentLocation[0]+delX, self.currentLocation[1]+delY], previousVisited = self.previousVisited + newVisit))
        return successorList
    



# The search method used is a standart depth first search, which should work fine but is very slow
# With a breadth first search, one would go through all the previous possible states (63 moves)
# before even testing a possibly correct solution. 
#
# Thus, 30 (number chosen as tradeoff between speed and number of repetitions) random moves are
# initialized, which 

DEBUG = True
def depthFirstSearch(initialState, victoryCondition, initialPath = []):
    numExpansions = 0 #the number of expanded states
    numVisited = 0 # the number of visited states
    minElapsed = 0

    # the time will be tracked
    print("Starting dfs")
    startTime = time.time()
    
    # depthFirst uses a Last In First Out queue; size is not limited
    myQueue = queue.LifoQueue(maxsize=0)
    
    print("Initial state: "+ str(initialState))
    myQueue.put( (initialState, initialPath) ) # put the initial state into the queue
    
    while not myQueue.empty():
        currentState, currentPath = myQueue.get() # get the next state from the queue
        numVisited += 1

        if victoryCondition(currentState): # check if goal state is reached
            stopTime = time.time()
            print("Goalstate reached after expanding {} times and visiting {} states!".format(numExpansions, numVisited))
            print("Time elapsed: {} h {:.1f} min".format( (stopTime-startTime)//3600, (stopTime-startTime)//60 ) )
            print(currentPath)
            return currentState, currentPath
                    
        
        # periodically gives updates (every minute) 
        numExpansions += 1
        if numVisited%1e5 == 0:
            if int( (time.time()-startTime)//60 ) > minElapsed:
                minElapsed += 1
                middleTime = time.time()
                print("Visited {} states in {}:{} min".format(numVisited, int((middleTime-startTime)//60), int((middleTime-startTime)%60)  ))

        for nextState in currentState.successors(): # put the successors in the queue
            myQueue.put( (nextState, currentPath + [nextState.currentLocation] ) )
    print("All states ({}) visited; none of them satisfied the goal condition".format(numVisited) )
    return initialState, []


def tryInitialize(state, numMoves): # initialize numMoves random moves from the given state   
    
    acceptable = False
    while not acceptable:
        newState = state
        newPath = [state.currentLocation]
        for i in range(numMoves):
            if newState.successors() == []:
                print("Ran into state with no successors while initializing. Starting over")
                break
            newState = np.random.choice(newState.successors())
            newPath.append(newState.currentLocation)
        if newState.successors() != []:# if acceptable : return it
            acceptable = True
        #if not acceptable: start over
    return newState, newPath
    

if __name__ == "__main__":
    
    foundPath = []
    trialCounter = 0
    randomStartTime = time.time()
    while foundPath == []:# Random search: we initialize 30 moves, the analysis afterwards should go fast for many states
        print()
        print("Try number {}".format(trialCounter+1))
        startState, startPath = tryInitialize(KnightState([0,0], includeCurrent=True), 30 )
        
        endState, foundPath = depthFirstSearch(startState,
                                lambda x: ( (x.previousVisited == np.ones([8,8], dtype=int)).all() ),
                                initialPath = startPath)
        trialCounter += 1
        
    np.save("foundPath.npy", foundPath)
    randomTimeDelta = time.time()-randomStartTime
    print("Found solution after {} trials in {} min {} s".format(trialCounter, int(randomTimeDelta//60), int(randomTimeDelta%60)) )
    
    ### Test outcome:
    ### Found solution after 237 trials in 172 min 20 s 
    ###    [[0, 0], [1, 2], [2, 0], [0, 1], [1, 3], [3, 4], [4, 6], [5, 4], [7, 3], [6, 1], [5, 3], [7, 2], [6, 0], [4, 1], [2, 2], [1, 0], [0, 2], [2, 3], [1, 5], [2, 7], [0, 6], [1, 4], [3, 3], [5, 2], [6, 4], [5, 6], [7, 7], [6, 5], [5, 7], [7, 6], [5, 5], [6, 7], [7, 5], [6, 3], [7, 1], [5, 0], [3, 1], [4, 3], [3, 5], [4, 7], [6, 6], [7, 4], [6, 2], [7, 0], [5, 1], [3, 0], [4, 2], [2, 1], [4, 0], [3, 2], [1, 1], [0, 3], [2, 4], [0, 5], [1, 7], [3, 6], [4, 4], [2, 5], [0, 4], [1, 6], [3, 7], [4, 5], [2, 6], [0, 7]]