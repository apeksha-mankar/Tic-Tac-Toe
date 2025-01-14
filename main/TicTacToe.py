#IMPORTS
import pygame as pg
import sys
import os

from pygame.locals import *

import time


# CONSTANTS
XO = 'x'
winner = None
draw = False
width = 400
height = 400
white = (255, 255, 255)
blue = (0, 0, 255)
black=(0,0,0)
line_color = (blue)

TTT = [[None]*3,[None]*3,[None]*3]

#INITIALIZATIONS
pg.init()
fps = 30
CLOCK = pg.time.Clock()
screen = pg.display.set_mode((width, height+100),0,32)
pg.display.set_caption("TIC-TAC-TOE")

# X AND O LAYOUT
#LOAD IMAGES
opening1 = pg.image.load('.././Images/TicTacToe_Opening1.png')
x_img = pg.image.load('.././Images/image_for_X.jpg')
o_img = pg.image.load('.././Images/image_for_O.jfif')

#TRANSFORM IMAGES
x_img = pg.transform.scale(x_img, (90,90))
o_img = pg.transform.scale(o_img, (90,90))
opening1 = pg.transform.scale(opening1, (width, height+100))

# INITIALIZING SCREEN
def game_opening():
    screen.blit(opening1,(0,0))
    pg.display.update()
    time.sleep(1)
    screen.fill(0)
    pg.draw.line(screen,line_color,(width/3,0),(width/3, height),5)
    pg.draw.line(screen,line_color,(width/3*2,0),(width/3*2, height),5)
    pg.draw.line(screen,line_color,(0,height/3),(width, height/3),5)
    pg.draw.line(screen,line_color,(0,height/3*2),(width, height/3*2),5)
    draw_status()


# FUNCTION TO GET STATUS
def draw_status():
    global draw
    if winner is None:
        message = XO.upper() + "'s Turn"
    else:
        message = winner.upper() + " Won!!... Congratulations!!"
    if draw:
        message = 'Game Draw!'
    font = pg.font.Font(None, 30)
    text = font.render(message, 1, (0, 255, 255))
    screen.fill ((0, 0, 0), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(width/2, 500-50))
    screen.blit(text, text_rect)
    pg.display.update()


# FUNCTION TO CHECK WINNER
def check_win():
    global TTT, winner,draw
    for row in range (0,3):
        if ((TTT [row][0] == TTT[row][1] == TTT[row][2]) and(TTT [row][0] is not None)):
            winner = TTT[row][0]
            pg.draw.line(screen, (150,0,0), (0, (row + 1)*height/3 -height/6), (width, (row + 1)*height/3 - height/6 ), 4)
            break
    for col in range (0, 3):
        if (TTT[0][col] == TTT[1][col] == TTT[2][col]) and (TTT[0][col] is not None):
            winner = TTT[0][col]
            pg.draw.line (screen, (150,0,0),((col + 1)* width/3 - width/6, 0), ((col + 1)* width/3 - width/6, height), 4)
            break
    if (TTT[0][0] == TTT[1][1] == TTT[2][2]) and (TTT[0][0] is not None):
        winner = TTT[0][0]
        pg.draw.line (screen, (150,70,70), (50, 50), (350, 350), 4)
    if (TTT[0][2] == TTT[1][1] == TTT[2][0]) and (TTT[0][2] is not None):
        winner = TTT[0][2]
        pg.draw.line (screen, (150,70,70), (350, 50), (50, 350), 4)
    if(all([all(row) for row in TTT]) and winner is None ):
        draw = True
    draw_status()


# FUNCTION TO PUT X OR O
def drawXO(row,col):
    global TTT,XO
    if row==1:
        posx = 30
    if row==2:
        posx = width/3 + 30
    if row==3:
        posx = width/3*2 + 30
    if col==1:
        posy = 30
    if col==2:
        posy = height/3 + 30
    if col==3:
        posy = height/3*2 + 30
    TTT[row-1][col-1] = XO
    if(XO == 'x'):
        screen.blit(x_img,(posy,posx))
        XO= 'o'
    else:
        screen.blit(o_img,(posy,posx))
        XO= 'x'
    pg.display.update()


# FUNCTION TO MOVE THE MOUSE OVER SCREEN
def userClick():
    x,y = pg.mouse.get_pos()
    if(x<width/3):
        col = 1
    elif (x<width/3*2):
        col = 2
    elif(x<width):
        col = 3
    else:
        col = None
    if(y<height/3):
        row = 1
    elif (y<height/3*2):
        row = 2
    elif(y<height):
        row = 3
    else:
        row = None
    if(row and col and TTT[row-1][col-1] is None):
        global XO
        drawXO(row,col)
        check_win()


def display_end_options():
    screen.fill(black, (0, 400, 500, 100))  # Clear the status area
    font = pg.font.Font(None, 25)
    draw_status()
    reset_button = font.render('Again :)', True, white)
    exit_button = font.render('Exit :(', True, white)
    
    # Calculate the x-coordinates for the buttons with a gap in between
    reset_button_x = width / 5
    exit_button_x = width / 3 + 105  # Add a gap of 100 pixels
    
    screen.blit(reset_button, (reset_button_x, height + 60))
    screen.blit(exit_button, (exit_button_x, height + 60))
    pg.display.update()
    
    return reset_button.get_rect(topleft=(reset_button_x, height + 60)), exit_button.get_rect(topleft=(exit_button_x, height + 60))


# FUNCTION TO HANDLE END OF GAME CHOICES
def handle_end_of_game(reset_rect, exit_rect):
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                x, y = event.pos
                if reset_rect.collidepoint(x, y):
                    reset_game()
                    return  # Exit the loop and restart the game
                elif exit_rect.collidepoint(x, y):
                    pg.quit()
                    sys.exit()


# FUNCTION TO RESET GAME
def reset_game():
    global TTT, winner,XO, draw
    time.sleep(1)
    XO = 'x'
    draw = False
    winner = None
    game_opening()
    winner=None
    TTT = [[None]*3,[None]*3,[None]*3]


# RUN THE GAME
game_opening()
while(True):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN: 
            userClick()
            if winner or draw:
                reset_rect, exit_rect = display_end_options()  # Show options
                handle_end_of_game(reset_rect, exit_rect)  # Handle user choice
    pg.display.update()
    CLOCK.tick(fps)