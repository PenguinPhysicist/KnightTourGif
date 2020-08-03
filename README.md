# KnightTourGif
Implementing a mix between random and depth-first-search, find a knight tour and create a GIF.

myKnights.py hosts the Knight tour algorithm, where 30 random moves are initialized and then a depth-first-search is done.
This is repeated until a suitable solution is found. Due to the construction of the KnightState class, every state can only be visited once.

In chessGraph.py, the GIF is constructed from a given path.
