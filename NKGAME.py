import pygame as pg
import numpy as np
import random
import RESOURCES

# Load up game resources so we can store data locally to the player as the game is going
game = RESOURCES.RESOURCES()

# Class to make a window
class NewWin:
    def __init__(self, width, height, color):
        self.width = width
        self.height = height
        self.color = color

        self.win = pg.display.set_mode((width, height))

    # Add a caption to the top of our window
    def AddCaption(self, caption):
        self.caption = caption
        pg.display.set_caption(self.caption)

    def disp(self):
        self.win.fill(self.color)
        if game.cam_activated:
            for rect in game.rects_cam:
                # If there is no image, draw the selected color of the rect
                if rect.image == None:

                    rect_surface = pg.Surface((rect.width, rect.height))
                    rect_surface.fill(rect.color)

                    rect.rect = pg.Rect(rect.x + rect.displacement_x,
                                        rect.y + rect.displacement_y,
                                        rect.width, rect.height)

                    self.win.blit(rect_surface, rect.rect)

                # If there is an image for the rect, draw the image onto the rect
                else:
                    rect.rect = pg.Rect(rect.x + rect.displacement_x,
                                        rect.y + rect.displacement_y,
                                        rect.width, rect.height)

                    self.win.blit(rect.image, (rect.rect.x, rect.rect.y))
        else:
            for rect in game.rects:
                # If there is no image, draw the selected color of the rect
                if rect.image == None:

                    rect_surface = pg.Surface((rect.width, rect.height))
                    rect_surface.fill(rect.color)

                    rect.rect = pg.Rect(rect.x, rect.y, rect.width, rect.height)
                    self.win.blit(rect_surface, rect.rect)

                # If there is an image for the rect, draw the image onto the rect
                else:
                    rect.rect = pg.Rect(rect.x, rect.y, rect.width, rect.height)
                    self.win.blit(rect.image, (rect.rect.x, rect.rect.y))

# Player class
class NewRect:
    def __init__(self, x, y, player_width, player_height, color, include_in_resc):
        self.x = x
        self.y = y
        self.width = player_width
        self.height = player_height
        self.color = color
        self.include_in_resc = include_in_resc

        self.displacement_x = 0
        self.displacement_y = 0

        self.rect = pg.Rect(x, y, self.width, self.height)

        self.image = None

        # If the player wants to include the rect in the resources list, append the rect to the list
        if self.include_in_resc == True:
            game.rects.append(self)
        else:
            pass

    # Make a function that adds an image on top of the rectangle
    def add_image(self, image_dir):
        self.image = pg.image.load(str(image_dir))

        # Scale the image t the size of the rect
        self.image = pg.transform.scale(self.image, (self.width, self.height))

# Class to add text in game easily
class AddText:
    def __init__(self, text, font, font_size, color, x, y):
        self.text = text
        self.font = font
        self.font_size = font_size
        self.color = color

        self.x = x
        self.y = y

        # Make a variable to store the font
        NewFont = pg.font.Font(str(self.font), int(self.font_size))

        # Render the font
        self.Text = NewFont.render(str(self.text), True, self.color)

        # Make a rect to display the text in
        self.TextRect = self.Text.get_rect()
        self.TextRect.center = (self.x, self.y)

    # Display our text
    def DisplayText(self, window):
        window.win.blit(self.Text, self.TextRect)

class NewButton:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

        self.button_rect = pg.Rect(self.x, self.y, self.width, self.height)
        self.button_surface = pg.Surface((self.width, self.height))

    def place(self, window):
        self.button_surface.fill(self.color)

        window.win.blit(self.button_surface, self.button_rect)

    def higlight_when_hovered(self, higlight_color):
        cursor = pg.mouse.get_pos()
        collide = self.button_rect.collidepoint(cursor)
        self.color = self.color if not collide else higlight_color

# Make a class that binds a camera to a player
class NewCam:
    def __init__(self):
        game.cam_activated = True

        self.displacement_x = 0
        self.displacement_y = 0

        for rect in game.rects:
            game.rects_cam.append(rect)

    # Make a function that binds the camera to a player
    def lock_to_player(self, player):
        self.player = player
        self.player_x = player.x
        self.player_y = player.y

    # Make a function to update the player and a ist of terrain rects
    def update_cam(self, displace_x, displace_y):
        self.displacement_x = self.player_x - self.player.x
        self.displacement_y = self.player_y - self.player.y

        for object in game.rects:
            if displace_x:
                object.displacement_x = self.displacement_x
            if displace_y:
                object.displacement_y = self.displacement_y

# Make a class to store a block of terrain
class TerrainBlock:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

        self.pos = (self.x, self.y)

# Class to make randomly generated terrain and display it as a list
class BuildTerrain:
    def __init__(self, width, height, terrain_height_limit, smoothing, values_list):
        self.width = width # Set how long we want our terrain to be

        self.height = height - 1 # Set this as the height of your window

        self.terrain_height_limit = terrain_height_limit # Set how tall we want the terrain to go up to
        self.terrain_height_limit = self.height - self.terrain_height_limit # Invert out terrain limit since numpy moves top to bottom

        self.ground = self.height - 1 # Set a ground variable so we always have a ground drawn on our screen

        self.area = self.width * self.height

        self.smoothing = smoothing # Set weather or not we want to smooth out the terrain

        self.values_list = values_list # Set a list of integers to randomly chose from and generate terrain

        # Make a list that has a set of 1's and 0's
        # If there is a 0, there will be a blank pixel, if there is a 1, there will be a block there
        self.Terrain = np.arange(int(self.area)).reshape(int(self.height), int(self.width))

        self.row = 0
        self.colum = 0

        for value in values_list:
            if value == 1:
                print('ERROR: Cannot have value "1" in list:', self.values_list)
                quit()
            else:
                pass

        # Make a for loop that goes through each block and randomly generates terrain
        for i in range(int(self.area)):
            rand = random.choice(self.values_list)
            if self.colum <= (self.width - 1):

                if self.row < self.terrain_height_limit:
                    self.Terrain[self.row, self.colum] = 0
                    self.colum += 1

                if self.row >= self.terrain_height_limit:
                    if self.row < self.ground:
                        if rand == self.values_list[1]:
                            self.Terrain[self.row, self.colum] = self.values_list[1]

                        if rand == self.values_list[0]:
                            self.Terrain[self.row, self.colum] = self.values_list[0]

                        self.colum += 1

            if self.row == self.ground:
                self.Terrain[self.row, self.colum] = 1 # Always have this as
                                                       # 1 for the floor
                self.colum += 1

            if self.colum == self.width:
                self.colum = 0
                self.row += 1

        if self.smoothing == True:
            for y, row in enumerate(self.Terrain):
                for x, value in enumerate(row):
                    if value == 0:
                        if x > 0 and self.Terrain[y, x - 1] == 1:
                            if x < self.width - 1 and self.Terrain[y, x + 1] == 1:
                                self.Terrain[y, x] = 1

                        if y > 0 and self.Terrain[y - 1, x] == 1:
                            if y < self.height - 1 and self.Terrain[y + 1, x] == 1:
                                self.Terrain[y, x] = 1

        if self.smoothing == False:
            pass

        self.array_bytes_size = self.Terrain.nbytes

    # Make a function that will go through each number in the "Terrain" array
    # If the value is a certain number, make a TerrainBlock object and
    # Store it in the games resources
    def check_array_for_blocks(self, block_value):
        for y, row in enumerate(self.Terrain[::1]):
            for x, value in np.ndenumerate(row):
                if value == block_value:
                    new_block = TerrainBlock(x[0], y, 'terrain_block')
                    game.terrain_blocks.append(new_block)
                # Check for which blocks are ground blocks
                if value == 1:
                    new_block = TerrainBlock(x[0], y, 'ground_block')
                    game.terrain_blocks.append(new_block)