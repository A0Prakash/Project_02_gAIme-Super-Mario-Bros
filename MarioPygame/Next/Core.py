#I ONLY EDITED THIS FILE(AARAV)
from os import environ

import pygame as pg
from pygame.locals import *

from Const import *
from Map import Map
from MenuManager import MenuManager
from Sound import Sound
from PIL import Image
import numpy as np
from Mario import Mario
import cv2
import random
from CustomWrappers import FrameStackWrapper, SkipFrameWrapper

class Core(object):
    """

    Main class.

    """
    def __init__(self):
        environ['SDL_VIDEO_CENTERED'] = '1'
        pg.mixer.pre_init(44100, -16, 2, 1024)
        pg.init()
        pg.display.set_caption('Mario by S&D')
        pg.display.set_mode((WINDOW_W, WINDOW_H))

        self.screen = pg.display.set_mode((WINDOW_W, WINDOW_H))
        self.clock = pg.time.Clock()

        self.oWorld = Map('1-1')
        self.oSound = Sound()
        self.oMM = MenuManager(self)

        self.run = True
        self.keyR = False
        self.keyL = False
        self.keyU = False
        self.keyD = False
        self.keyShift = False

    #I modified this to implement framestack and skipframe wrappers from gym
    #This is the function(where the magic happens)
    def main_loop(self):
        #Import the Agent(Mario)
        mario = Mario(input_dims = (4,84,84), num_actions = 5)
        mario.load_model("Models/3_iter.pt")
        
        #Iteration number(used to skipping once every 4 frames)
        i=0
        #Queue for framestacking
        framequeue = []
        self.input(0)
        while self.run:
            if self.get_mm().currentGameState == 'Game':
                #if its the fourth frame(skipframe(4))
                if(i == 3):
                    #get the pygame image and add the gym grayscale and resize wrappers
                    image_data = pg.surfarray.array3d(pg.display.get_surface()) 
                    arr = self.getCroppedImg(image_data)
                    #add the array to the framequeue
                    framequeue.append(arr)
                    #when framequeue fills up
                    if(len(framequeue) == 4):
                        #print("YEAEYAEFGSYDFG")
                        #turn framequeue into a numpy array that can be passed into model
                        #stacks 4 on top of each other to make an array of size (4,84,84)
                        framestack = np.dstack(framequeue)
                        framestack = np.rollaxis(framestack,-1)
                        #print(framestack.shape)
                        #input it into model
                        self.input(mario.choose_action(framequeue))
                        #remove the first element of framestack(the first so that another can be added later)
                        framequeue.pop(0)
                    i=0
                i = i + 1
            else:
                self.input(0)
            self.update()
            self.render()
            self.clock.tick(FPS)

    #getCroppedImg function: it takes an image and grayscales/resizes it for the agent
    def getCroppedImg(self, img):
        #get the image
        img = Image.fromarray(img, 'RGB')
        #rotate it
        img = img.transpose(Image.TRANSPOSE)
        #crop it
        img = img.crop((190, 0, 610, 448))
        arr = np.array(img)
        #re rotate it
        arr = np.swapaxes(arr, 0, 1)
        #resize it to (84,84)
        arr = cv2.resize(arr, (84,84), interpolation = cv2.INTER_LINEAR)
        #grayscale it
        arr = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)
        return arr
        
    def input(self, op):
        if self.get_mm().currentGameState == 'Game':
            self.input_player(op)
        else:
            self.input_menu()

    #modified this function to use the inputs as an int that are in gym enviroment
    #ints represent right_only of gym_super_mario_bros
    def input_player(self, op):
        if(op == 0):
            self.keyR = False
            self.keyShift = False
            self.keyU = False
        elif(op == 1):
            self.keyR = True
            self.keyShift = False
            self.keyU = False
        elif(op == 2):
            self.keyR = True
            self.keyU = True
            self.keyShift = False
        elif(op == 3):
            self.keyR = True
            self.keyU = False
            self.keyShift = True
        elif(op == 4):
            self.keyR = True
            self.keyU = True
            self.keyShift = True

        #     elif e.type == KEYDOWN:
        #         if e.key == K_RIGHT:
        #             self.keyR = True
        #         elif e.key == K_LEFT:
        #             self.keyL = True
        #         elif e.key == K_DOWN:
        #             self.keyD = True
        #         elif e.key == K_UP:
        #             self.keyU = True
        #         elif e.key == K_LSHIFT:
        #             self.keyShift = True

        #     elif e.type == KEYUP:
        #         if e.key == K_RIGHT:
        #             self.keyR = False
        #         elif e.key == K_LEFT:
        #             self.keyL = False
        #         elif e.key == K_DOWN:
        #             self.keyD = False
        #         elif e.key == K_UP:
        #             self.keyU = False
        #         elif e.key == K_LSHIFT:
        #             self.keyShift = False

    def input_menu(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.run = False

            elif e.type == KEYDOWN:
                if e.key == K_RETURN:
                    self.get_mm().start_loading()

    def update(self):
        self.get_mm().update(self)

    def render(self):
        self.get_mm().render(self)

    def get_map(self):
        return self.oWorld

    def get_mm(self):
        return self.oMM

    def get_sound(self):
        return self.oSound
