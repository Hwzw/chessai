import chess as chess
import math
import numpy as np
import pandas as pd
import pygame as pg
import tensorflow as tf
from tensorflow import keras
from scipy.special import expit
import cnn_model
from cnn_model import board_to_list
from cnn_model import AiEval
import minmax
from minmax import alpha_beta
from minmax import get_best_move
from minmax import evaluate

#initialise display
X = 800
Y = 800
scrn = pg.display.set_mode((X, Y))
pg.init()

#basic colours
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
YELLOW = (204, 204, 0)
BLUE = (50, 255, 255)
GREEN = (0,150, 0)
BLACK = (0, 0, 0)

#initialise chess board
b = chess.Board()

#load piece images
pieces = {'p': pg.transform.smoothscale(pg.image.load('b_pawn.png'), (80,80)),
          'n': pg.transform.smoothscale(pg.image.load('b_knight.png'), (80,80)),
          'b': pg.transform.smoothscale(pg.image.load('b_bishop.png'), (80,80)),
          'r': pg.transform.smoothscale(pg.image.load('b_rook.png'), (80,80)),
          'q': pg.transform.smoothscale(pg.image.load('b_queen.png'), (80,80)),
          'k': pg.transform.smoothscale(pg.image.load('b_king.png'), (80,80)),
          'P': pg.transform.smoothscale(pg.image.load('w_pawn.png'), (80,80)),
          'N': pg.transform.smoothscale(pg.image.load('w_knight.png'), (80,80)),
          'B': pg.transform.smoothscale(pg.image.load('w_bishop.png'), (80,80)),
          'R': pg.transform.smoothscale(pg.image.load('w_rook.png'), (80,80)),
          'Q': pg.transform.smoothscale(pg.image.load('w_queen.png'), (80,80)),
          'K': pg.transform.smoothscale(pg.image.load('w_king.png'), (80,80)),
          
          }

def update(scrn,board):
    '''
    updates the screen basis the board class
    '''
    
    for i in range(64):
        piece = board.piece_at(i)
        if piece == None:
            pass
        else:
            scrn.blit(pieces[str(piece)],((i%8)*100+10,700-(i//8)*100+10))
    
    for i in range(7):
        i=i+1
        pg.draw.line(scrn,WHITE,(0,i*100),(800,i*100))
        pg.draw.line(scrn,WHITE,(i*100,0),(i*100,800))

    pg.display.flip()

def main(BOARD):

    '''
    for human vs human game
    '''
    #make background black
    scrn.fill(GREEN)
    #name window
    pg.display.set_caption('Chess')
    
    #variable to be used later
    index_moves = []

    status = True
    while (status):
        #update screen
        update(scrn,BOARD)

        for event in pg.event.get():
     
            # if event object type is QUIT
            # then quitting the pg
            # and program both.
            if event.type == pg.QUIT:
                status = False

            # if mouse clicked
            if event.type == pg.MOUSEBUTTONDOWN:
                #remove previous highlights
                scrn.fill(GREEN)
                #get position of mouse
                pos = pg.mouse.get_pos()

                #find which square was clicked and index of it
                square = (math.floor(pos[0]/100),math.floor(pos[1]/100))
                index = (7-square[1])*8+(square[0])
                
                # if we are moving a piece
                if index in index_moves: 
                    
                    move = moves[index_moves.index(index)]
                    
                    BOARD.push(move)

                    #reset index and moves
                    index=None
                    index_moves = []
                    
                    
                # show possible moves
                else:
                    #check the square that is clicked
                    piece = BOARD.piece_at(index)
                    #if empty pass
                    if piece == None:
                        
                        pass
                    else:
                        
                        #figure out what moves this piece can make
                        all_moves = list(BOARD.legal_moves)
                        moves = []
                        for m in all_moves:
                            if m.from_square == index:
                                
                                moves.append(m)

                                t = m.to_square

                                TX1 = 100*(t%8)
                                TY1 = 100*(7-t//8)

                                
                                #highlight squares it can move to
                                pg.draw.rect(scrn,BLUE,pg.Rect(TX1,TY1,100,100),5)
                        
                        index_moves = [a.to_square for a in moves]
     
    # deactivates the pygame library
        if BOARD.outcome() != None:
            print(BOARD.outcome())
            status = False
            print(BOARD)
    pg.quit()

def against_ai(BOARD,agent,agent_color, depth):
    
    '''
    for agent vs human game
    color is True = White agent
    color is False = Black agent
    '''
    
    #make background black
    scrn.fill(GREEN)
    #name window
    pg.display.set_caption('Chess')
    
    #variable to be used later
    index_moves = []

    status = True
    while (status):
        #update screen
        update(scrn,BOARD)
        
     
        if BOARD.turn==agent_color:
            BOARD.push(agent(BOARD, depth))
            scrn.fill(GREEN)

        else:

            for event in pg.event.get():
         
                # if event object type is QUIT
                # then quitting the pg
                # and program both.
                if event.type == pg.QUIT:
                    status = False

                # if mouse clicked
                if event.type == pg.MOUSEBUTTONDOWN:
                    #reset previous screen from clicks
                    scrn.fill(GREEN)
                    #get position of mouse
                    pos = pg.mouse.get_pos()

                    #find which square was clicked and index of it
                    square = (math.floor(pos[0]/100),math.floor(pos[1]/100))
                    index = (7-square[1])*8+(square[0])
                    
                    # if we have already highlighted moves and are making a move
                    if index in index_moves: 
                        
                        move = moves[index_moves.index(index)]
                        #print(BOARD)
                        #print(move)
                        BOARD.push(move)
                        index=None
                        index_moves = []
                        
                    # show possible moves
                    else:
                        
                        piece = BOARD.piece_at(index)
                        
                        if piece == None:
                            
                            pass
                        else:

                            all_moves = list(BOARD.legal_moves)
                            moves = []
                            for m in all_moves:
                                if m.from_square == index:
                                    
                                    moves.append(m)

                                    t = m.to_square

                                    TX1 = 100*(t%8)
                                    TY1 = 100*(7-t//8)

                                    
                                    pg.draw.rect(scrn,BLUE,pg.Rect(TX1,TY1,100,100),5)
                            #print(moves)
                            index_moves = [a.to_square for a in moves]
     
    # deactivates the pygame library
        if BOARD.outcome() != None:
            print(BOARD.outcome())
            status = False
            print(BOARD)
    pg.quit()

def ai_vs_ai(BOARD,agent1,agent_color1,agent2, depth):
    '''
    for agent vs agent game
    
    '''
  
    #make background black
    scrn.fill(GREEN)
    #name window
    pg.display.set_caption('Chess')
    
    #variable to be used later

    status = True
    while (status):
        #update screen
        update(scrn,BOARD)
        
        if BOARD.turn==agent_color1:
            BOARD.push(agent1(BOARD, depth))

        else:
            BOARD.push(agent2(BOARD, depth))

        scrn.fill(GREEN)
            
        for event in pg.event.get():
     
            # if event object type is QUIT
            # then quitting the pg
            # and program both.
            if event.type == pg.QUIT:
                status = False
     
    # deactivates the pygame library
        if BOARD.outcome() != None:
            print(BOARD.outcome())
            status = False
            print(BOARD)
    pg.quit()
