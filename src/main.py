#! /usr/bin/python
# -*- coding: utf-8 -*-

import pyglet
from pyglet.gl import *

import math
import sys

import simu
import fabrique
import ihm

flag_fullscreen = False
flag_resizable  = True

try:
	config = Config(sample_buffer=1, samples=4, depth_size=16, double_buffer=True)
	window = pyglet.window.Window(resizable=True, config=config)
	#window = pyglet.window.Window(fullscreen=flag_fullscreen,resizable=flag_resizable)
except:
	window = pyglet.window.Window(fullscreen=flag_fullscreen,resizable=flag_resizable)



leMonde      = simu.Monde()
laFabrique   = fabrique.Fabrique(leMonde)
lInteracteur = ihm.Wimp(leMonde)

laFabrique.fabriquer()


def setup():
	glEnable(GL_DEPTH_TEST)
	glEnable(GL_TEXTURE_2D)
	glAlphaFunc(GL_GREATER,0.4)
	glEnable(GL_ALPHA_TEST)
	glEnable(GL_CULL_FACE)


@window.event
def on_resize(width, height):
	# Override the default on_resize handler to create a 3D projection
	glViewport(0, 0, width, height)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(70.0, width / float(height), .1, 1000.)
	glMatrixMode(GL_MODELVIEW)
	return pyglet.event.EVENT_HANDLED

@window.event
def on_draw():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	leMonde.dessiner() 

@window.event
def on_key_press(symbol,modifiers):
	lInteracteur.on_key_press(symbol)

	
@window.event
def on_key_release(symbol,modifiers):
	lInteracteur.on_key_release(symbol)

	
@window.event
def on_mouse_press(x,y,bouton,modifiers):
	pass

@window.event
def on_mouse_drag(x,y,dx,dy,boutons,modifiers):	
	lInteracteur.on_mouse_drag(x,y,dx,dy)
	
def updateRapide(dt):
	lInteracteur.actualiser(dt)
	leMonde.actualiser(dt)

def updateLent(dt):
	pass

      
import sys

if __name__ == "__main__":
	print ">> ", sys.argv
	setup()
	pyglet.clock.schedule_interval(updateRapide, 1.0/30.0)
	pyglet.clock.schedule_interval(updateLent,1.0/10.0)
	pyglet.app.run()


