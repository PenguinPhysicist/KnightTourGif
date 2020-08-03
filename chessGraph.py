# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 17:54:20 2019

@author: Philipp
"""
import os

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patheffects as PathEffects
import matplotlib.image as matimg

from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image

if not os.path.exists("walk/"):
    os.mkdir("walk/")

# load the obtained path
victoryPath = np.load("foundPath.npy")

def plotChessboard(path):
    board = np.zeros([8,8])
    for i in range(8):
        for j in range(8):
            if (i+j) %2 == 0:
                board[i,j] = 1
                
    knightToken = matimg.imread("knightToken.png")
    knightBox = OffsetImage(knightToken, zoom=0.03)

    plt.figure("Chessboard", figsize = (5.5,5.5))
    for i in range(len(path)+1):
        plt.clf()
        thisPath = path[:i].T
        #print(thisPath, len(thisPath[0]))
        ax = plt.subplot(1,1,1)
        ax.set_xticks(range(8))
        ax.set_xticklabels(["A", "B", "C", "D", "E", "F", "G", "H"])
        ax.imshow(board, cmap="Wistia", origin="lower", alpha = 1.)
        if len(thisPath[0])>0: # if there is a position for the knight to jump to yet
            knightAnBox = AnnotationBbox(knightBox, (thisPath[0,-1],thisPath[1,-1]), frameon=False,pad = 0.001)
            ax.add_artist(knightAnBox)
            if len(thisPath[0])>1: # if there are previously visited positions in the path
                
                for j in range(len(thisPath[0])-1):
                    ax.scatter(thisPath[0,j], thisPath[1,j], marker="${}$".format(j+1), s=420, edgecolors = "black", facecolors = "white", linewidth = 1, alpha=1) 
                            
        txt = plt.text(-0.42,-0.1,"Start", fontsize=10, color = "white", weight = "bold")
        txt.set_path_effects([PathEffects.withStroke(linewidth=4, foreground='black')])
        plt.draw()
        plt.savefig("walk/chessPath{}.png".format(i))
    imgs = [Image.open("walk/chessPath{}.png".format(i)) for i in range(len(path)) ]
    
    imgs[0].save("walk/chesswalk.gif", save_all=True, append_images=imgs[1:], duration = 1000, loop=0 ) 
    

plotChessboard(np.array(victoryPath)[1:])