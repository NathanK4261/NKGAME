# Import modules
import pygame as pg

from NKGAME import *

import NKNET

import time

pg.init()

# Player variables
p_x = 350
p_y = 350

p_width = 100
p_height = 100

p_vel = 3.5
moving = False

# Make a variable to store the position of the online player 2
p2_pos = None

# Make a list of all terrain blocks and all rectangles
terrain_blocks = []
ground_blocks = []
rects = []

# Server variables
ip = '192.168.158.117'
port = 5555
local_id = ''

# Set up the screen
width = 900
height = 900

# Add a path to the font we are using
arial = 'resources/fonts/arial.ttf'

sc = NewWin(width, height, 'black')
sc.AddCaption('Barebones: By Nathan Keidel')

# Add terrain
terrain = BuildTerrain(width, 9, 2, True, [0,2])
terrain.check_array_for_blocks(2)

for block in game.terrain_blocks:
    block = NewRect(block.x * 100, block.y * 100, 100, 100, 'white', True)

    game.rects.append(block)

# Update window function
def update_window(window, cam, player):
    window.win.fill(window.color)

    # Update our camera
    cam.update_cam(True, True)

    # Display all the updates to the window
    window.disp()

    # Update the display
    pg.display.update()

# Function to move our player by a certain velocity
def move_player(player, vel):
    keys = pg.key.get_pressed()

    if keys[pg.K_a]:
        player.x -= vel

    if keys[pg.K_d]:
        player.x += vel

    if keys[pg.K_w]:
        player.y -= vel

    if keys[pg.K_s]:
        player.y += vel

def run_game():
    # Set globals
    global p_x
    global p_y

    # Set variable "run" as false to begin setup
    run = False
    menu = True

    # Wait for "StartPosUpdate"
    while menu:
        # Make a main menu
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                break
            if event.type == pg.MOUSEBUTTONUP:
                cursor = pg.mouse.get_pos()
                collide = start_button.button_rect.collidepoint(cursor)

                if collide:
                    menu = False

                    loading_text = AddText('Loading into game...', arial, 60, 'white', 450, 730)
                    loading_text.DisplayText(sc)

                    loading_text = AddText(f'IP:  {ip}, PORT: {port}', arial, 20, 'white', 450, 830)
                    loading_text.DisplayText(sc)
                else:
                    pass

            start_button_outline = NewButton(225, 422, 450, 180, (0, 0, 0))
            start_button_outline.higlight_when_hovered((225, 225, 0))
            start_button_outline.place(sc)

            start_button = NewButton(250, 450, 400, 130, (0, 220, 0))
            start_button.higlight_when_hovered((0, 220, 0))
            start_button.place(sc)

            start_text = AddText('Click to start', arial, 60, 'white', 450, 530)
            start_text.DisplayText(sc)

            start_text2 = AddText('Barebones', arial, 60, 'white', 450, 130)
            start_text2.DisplayText(sc)

            start_text3 = AddText('A game by Nathan Keidel', arial, 60, 'white', 450, 230)
            start_text3.DisplayText(sc)

            pg.display.update()

    while not run:
        # Start our client
        client = NKNET.network(ip, port, local_id)

        client.recv()

        # When the client connects to the server,
        if client.recv_data == None:
            print('INIT: CheckStat')
            client.send('CheckStat')
            print('Sent: CheckStat')

        if client.recv_data == 'StartPosUpdate':
            print('Starting game!')
            time.sleep(2)
            run = True

    # Define our players
    player1 = NewRect(p_x, p_y, p_width, p_height, (255,0,0), True)

    player2 = NewRect(0, 0, p_width, p_height, (0, 0, 255), True)

    # Make a camera
    cam = NewCam()

    # Lock our camera to player1
    cam.lock_to_player(player1)

    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                client.send('Quit')
                run = False
                pg.quit()

        # Make a "player1_pos" var so we can cleanly send the position data to the server
        player1_pos = (player1.x, player1.y)

        client.send(str(player1_pos))

        client.recv()

        if client.recv_data == 'QUIT':
            pg.quit()
            break
            quit()
        else:
            p2_pos = client.recv_data
            p2_pos = (tuple(map(float, p2_pos.strip("()").split(","))))

            (player2.x, player2.y) = p2_pos

            # Move our character
            move_player(player1, p_vel)

            # Update our window
            update_window(sc, cam, player1)

run_game()