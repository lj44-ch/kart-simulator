from os import path
from posixpath import abspath
from re import S
from sys import hexversion
import time
import os.path
from typing import List
from os import listdir
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout


from lib import Point
import client
from game.objects import *
import game

from io_objects.io_polygon import IO_Polygon
from io_objects.io_circle import IO_Circle

from kivy.utils import get_color_from_hex, rgba
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.properties import Clock
from kivy.properties import StringProperty


class PauseMode(FloatLayout):
    def __init__(self,width,height, music, **kwargs):
        
        self.chosen_music = str(music)
        self.width = width
        self.height = height
        super().__init__(**kwargs)
    
    def changeMusicSpinnerText(self,text):
        self.chosen_music = text
        
    def generateMusicsList(self):
        music_list = list(music[:-4] for music in listdir("client/sounds/music"))
        music_list.append("No music")
        return music_list


Builder.load_file("layouts.kv")



class MainWidget(Widget):
    from user_actions import (
    keyboard_closed,
    on_keyboard_down,
    # on_touch_up,
    on_keyboard_up,
    # on_touch_down,
    )
    dict_polygons = dict()
    dict_circles = dict()
    dict_finishLine = dict()
    kart_ID = 0
    
    
    def __init__(self,world=None, parentScreen=None, **kwargs):
        super().__init__(**kwargs)
        self.world = world
        self.parentScreen = parentScreen
        if isinstance(self.world,StringProperty):
            self.world = "2triangles"
            
        ##################### Création de la partie #####################
        dataUrl = path.join("client/worlds", self.world) + ".json"
        print(f"GameData: {dataUrl}")
        self.eventsList = list()

        from game.objects import Circle, Object
        from lib import Point

        self.theGame = game.Game(dataUrl, self.eventsList, self.output)
        print("Starting ...")

        print("Finisched!")
        #################################################################
        self.fps = 60

        self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
        self._keyboard.bind(on_key_down=self.on_keyboard_down)
        self._keyboard.bind(on_key_up=self.on_keyboard_up)

        self.my_clock = Clock
        self.my_clock.schedule_interval(self.theGame.nextFrame, 1 / self.fps)

        
        self.play = True
        
    def clear(self):
        print("LEAVED")
        self.canvas.clear()
        if self.play:
            self.my_clock.unschedule(self.theGame.nextFrame)
            
    def change_gameState(self):
        if self.play:
            # self.pause()
            self.parent.parent.pauseMode()
        else:
            # self.resume()
            self.parent.parent.resumeGame()

        
        

    def output(self, objects: List[game.objects.Object]):
        for object in objects:
            self.updateObstacle(obstacle=object)

    def updateObstacle(self, obstacleID=None, obstacle=None):
        if obstacleID or obstacleID == 0:
            obs = self.dict_polygons.get(obstacleID)
            io_obs = self.instanciateObstacle(obs)
        elif obstacle:
            obs = obstacle
            io_obs = self.instanciateObstacle(obs)

        if isinstance(obs,Circle):
            new_pos = obs.center()

        elif isinstance(obs,Polygon):
            new_pos = obs.vertices()

        io_obs.updatePosition(newPos=new_pos)

        if (
            obs._fill != io_obs.color
        ):  # En cas de changement de couleur de l'obstacle, kivy nous oblige à le redessiner
            self.canvas.remove(io_obs)
            if isinstance(obs,Circle):
                self.dict_circles.pop(obs.formID())
            elif isinstance(obs,Polygon):
                self.dict_polygons.pop(obs.formID())
                
            self.instanciateObstacle(obstacle=obs)



    def instanciateObstacle(self, obstacle=None):
        if obstacle:
            if (
                isinstance(obstacle,Circle)
                and obstacle.formID() not in self.dict_circles
            ):
                # with self.canvas.before:
                self.color = get_color_from_hex(obstacle._fill)
                with self.canvas:
                    Color(rgba=self.color)
                pos_x = obstacle.center()[0] - obstacle.radius()
                pos_y = obstacle.center()[1] - obstacle.radius()
                io_obstacle = IO_Circle(
                    diametre=2 * obstacle.radius(),
                    position=[pos_x, pos_y],
                    couleur=obstacle._fill,
                )
                self.canvas.add(io_obstacle)
                self.dict_circles[obstacle.formID()] = io_obstacle

            elif isinstance(obstacle,Circle):
                io_obstacle = self.dict_circles.get(obstacle.formID())

            elif (
                isinstance(obstacle,Polygon)
                and obstacle.formID() not in self.dict_polygons
            ):
                if type(obstacle).__name__ == "FinishLine":
                    with self.canvas:
                        finish_line = Rectangle(pos=obstacle.pos(), size=obstacle.size(), source="client/images/finish_line.jpg")
                    self.dict_finishLine[obstacle.formID()] = finish_line
                else:
                    if type(obstacle).__name__ == "Kart":
                        self.kart_ID = obstacle.formID()
                    
                    self.color = get_color_from_hex(obstacle._fill)
                    with self.canvas:
                        Color(rgba=self.color)
                    io_obstacle = IO_Polygon(
                        summits=obstacle.vertices(), couleur=obstacle._fill
                    )
                    self.canvas.add(io_obstacle)
                    self.dict_polygons[obstacle.formID()] = io_obstacle
            
            elif isinstance(obstacle,Polygon):
                io_obstacle = self.dict_polygons.get(obstacle.formID())
            return io_obstacle

