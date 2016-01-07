
import pyglet
from pyglet.gl import *

import math



class Wimp : 

	def __init__(self,monde):
		self.monde = monde
		self.camera = self.monde.camera
		self.enAvant     = False
		self.enArriere   = False
		self.versHaut    = False
		self.versBas     = False
		self.aGauche     = False
		self.aDroite     = False
		self.surgauche   = False
		self.surDroite   = False

	def actualiser(self,dt):
		if self.enAvant : 
			self.camera.avancer(0.25)
		elif self.enArriere : 
			self.camera.avancer(-0.25)
		elif self.versHaut : 
			self.camera.monter(0.1)
		elif self.versBas : 
			self.camera.monter(-0.1)
		elif self.aGauche :
			self.camera.gauche(0.1)
		elif self.aDroite :
			self.camera.gauche(-0.1)

		else:
			pass

	def on_key_press(self,symbol):
		if symbol == pyglet.window.key.SPACE :
			pass
		elif symbol == pyglet.window.key.UP : 
			self.enAvant = True
		elif symbol == pyglet.window.key.DOWN : 
			self.enArriere = True
		elif symbol == pyglet.window.key.LEFT : 
			self.aGauche = True
		elif symbol == pyglet.window.key.RIGHT : 
			self.aDroite = True
		elif symbol == pyglet.window.key.H :
			self.versHaut = True
		elif symbol == pyglet.window.key.B : 
			self.versBas  = True 
		elif symbol == pyglet.window.key.T : 
			self.monde.notifier()
		else:
			pass

	def on_key_release(self,symbol):
		if symbol == pyglet.window.key.SPACE :
			pass
		elif symbol == pyglet.window.key.UP : 
			self.enAvant = False
		elif symbol == pyglet.window.key.DOWN : 
			self.enArriere=False
		elif symbol == pyglet.window.key.LEFT : 
			self.aGauche = False
		elif symbol == pyglet.window.key.RIGHT : 
			self.aDroite = False
		elif symbol == pyglet.window.key.H :
			self.versHaut = False
		elif symbol == pyglet.window.key.B : 
			self.versBas  = False
		else:
			pass


	def on_mouse_drag(self,x,y,dx,dy):
		#print "DX = ", dx
		if dx < -1 : 
			self.camera.tourner(math.pi/180.0)
		elif dx > 1 : 
			self.camera.tourner(-math.pi/180.0)
			

