
import pyglet
from pyglet.gl import *

import wavefront

import geo

class TextureCatalog(object):
	_instance = None
	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(TextureCatalog, cls).__new__(
					cls, *args, **kwargs)
		return cls._instance

	def __init__(self):
		self.catalog = {}

	def loadTexture(self,nom,alias=None):

		if self.catalog.has_key(nom):
			if alias != None :
				self.catalog[alias] = self.catalog[nom]
			return self.catalog[nom]
		else:
			image = pyglet.image.load(nom)
			texture = image.get_texture()
			glBindTexture(GL_TEXTURE_2D,texture.id)
			glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
			glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
			glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
			self.catalog[nom] = texture
			if alias != None :
				self.catalog[alias] = self.catalog[nom]
				print "@@" , self.catalog[alias]
			return texture

def charger_texture(nom,alias=None):
	texture = TextureCatalog().loadTexture(nom)
	if alias != None :
		TextureCatalog().catalog[alias] = texture
	print "@!!@ ", TextureCatalog().catalog.keys()
	return texture


# =====================================================================================		

class Camera : 

	def __init__(self):
		self.repere = geo.Repere()
		self.repere.placer(geo.Vec3((-5.0,0.0,1.6)))
		self.repere.orienter(0.0)


	def lookAt(self):
		tx,ty,tz = self.repere.o.getCoordonnees()
		dx,dy,dz = self.repere.u.getCoordonnees()
		glLoadIdentity()
		gluLookAt(tx,ty,tz,tx+dx,ty+dy,tz+dz,0.0,0.0,1.0)
		
	def placer(self,p):
	  self.repere.placer(p)
	
	def orienter(self,cap):
	  self.repere.orienter(cap)
		
	def avancer(self,dl):
	  self.repere.avancer(dl)
	
	def monter(self,dh):
	  self.repere.monter(dh)
	
	def gauche(self,dl):
	  self.repere.gauche(dl)
	
	def tourner(self,dCap):
	  self.repere.tourner(dCap)

# =====================================================================================

class Objet : 
  
  def __init__(self, repere=None, maillage=None):
    if repere == None :
      self.repere = geo.Repere()
    else:
      self.repere = repere
      
    self.maillage = maillage
    
  def placer(self,p):
    self.repere.placer(p)
    
  def orienter(self,cap):
    self.repere.orienter(cap)
    
  def avancer(self,dl):
    self.repere.avancer(dl)
	
  def monter(self,dh):
    self.repere.monter(dh)
	
  def gauche(self,dl):
    self.repere.gauche(dl)
	
  def tourner(self,dCap):
    self.repere.tourner(dCap)
    
  def dessiner(self):
    if self.maillage != None :
      tx, ty, tz = self.repere.o.getCoordonnees()
      cap        = self.repere.angleDegre
      glPushMatrix()
      glTranslatef(tx,ty,tz)
      glRotatef(cap, 0.0,0.0,1.0)
      self.maillage.draw()
      glPopMatrix()
      

# =====================================================================================		
class Maillage : 

	def __init__(self):
		self.perceptible = True


	def draw(self):
		pass

# =====================================================================================	 

class Sphere(Maillage):

	def __init__(self,**attributs):
		Maillage.__init__(self)
		self.radius = attributs.get('radius',1.0)
		self.slices = attributs.get('slices',30)
		self.stacks = attributs.get('stacks',30)

	def draw(self):
		q = gluNewQuadric()
		gluQuadricDrawStyle(q,GLU_FILL)
		gluSphere(q,self.radius,self.slices,self.stacks)
		gluDeleteQuadric(q)

# =====================================================================================

class Triedre(Maillage):

	def __init__(self,l):
		Maillage.__init__(self)
		self.l = l

	def draw(self):
		glDisable(GL_TEXTURE_2D)
		glBegin(GL_LINES)
		glColor3f(1.0,0.0,0.0)
		glVertex3f(0.0,0.0,0.0)
		glVertex3f(self.l,0.0,0.0)
		glColor3f(0.0,1.0,0.0)
		glVertex3f(0.0,0.0,0.0)
		glVertex3f(0.0,self.l,0.0)
		glColor3f(0.0,0.0,1.0)
		glVertex3f(0.0,0.0,0.0)
		glVertex3f(0.0,0.0,self.l)
		glEnd()
		glEnable(GL_TEXTURE_2D)

# =====================================================================================

class Panneau(Maillage):
  
	def __init__(self,**attributs):
		Maillage.__init__(self)
		self.visible = True
		recto = attributs.get('recto',"../data/textures/acajou.png")
		self.recto = TextureCatalog().loadTexture(recto)
		verso = attributs.get('verso',"../data/textures/moquette.jpg")
		self.verso = TextureCatalog().loadTexture(verso)
		self.largeur = attributs.get('largeur',1.0)
		self.hauteur = attributs.get('hauteur',1.0)
		self.epaisseur = attributs.get('epaisseur',0.01)
		
	def draw(self):
		if self.perceptible : 
			glPushMatrix()
			glTranslatef(0.0,- self.epaisseur/2.0,0.0)
			glScalef(self.largeur,self.epaisseur,self.hauteur)
			
			glBindTexture(GL_TEXTURE_2D,self.recto.id)
			glBegin(GL_QUADS)
			glTexCoord2f(0.0, 0.0)
			glVertex3f(1.0,1.0,0.0)
			glTexCoord2f(1.0, 0.0)
			glVertex3f(0.0, 1.0, 0.0)
			glTexCoord2f(1.0, 1.0)
			glVertex3f(0.0, 1.0, 1.0)
			glTexCoord2f(0.0, 1.0)
			glVertex3f(1.0, 1.0, 1.0)
			glEnd()
			
			glBindTexture(GL_TEXTURE_2D,self.verso.id)
			glBegin(GL_QUADS)
			glTexCoord2f(0.0, 0.0)
			glVertex3f(0.0,0.0,0.0)
			glTexCoord2f(1.0, 0.0)
			glVertex3f(1.0, 0.0, 0.0)
			glTexCoord2f(1.0, 1.0)
			glVertex3f(1.0, 0.0, 1.0)
			glTexCoord2f(0.0, 1.0)
			glVertex3f(0.0, 0.0, 1.0)
			glEnd()
			
			glPopMatrix()
			
# =====================================================================================			

class Tableau(Maillage) : 
	def __init__(self,**attributs):
		Maillage.__init__(self)
		self.visible = True
		recto = attributs.get('recto',"../data/textures/dante.jpg")
		self.recto = TextureCatalog().loadTexture(recto)
		verso = attributs.get('verso',"../data/textures/dante.jpg")
		self.verso = TextureCatalog().loadTexture(verso)
		self.largeur = attributs.get('largeur',1.0)
		self.hauteur = attributs.get('hauteur',1.0)
		self.epaisseur = attributs.get('epaisseur',0.01)

	def draw(self):
		if self.perceptible:
			glPushMatrix()
			glScalef(self.epaisseur,self.largeur/2.0,self.hauteur/2.0)

			glBindTexture(GL_TEXTURE_2D,self.recto.id)
			glBegin(GL_QUADS)
			glTexCoord2f(0.0, 0.0)
			glVertex3f(1.0, -1.0, -1.0)
			glTexCoord2f(1.0, 0.0)
			glVertex3f(1.0, 1.0, -1.0)
			glTexCoord2f(1.0, 1.0)
			glVertex3f(1.0, 1.0, 1.0)
			glTexCoord2f(0.0, 1.0)
			glVertex3f(1.0, -1.0, 1.0)
			glEnd()

			glBindTexture(GL_TEXTURE_2D,self.verso.id)

			glBegin(GL_QUADS)
			glTexCoord2f(0.0, 0.0)
			glVertex3f(0.0, 1.0, -1.0)
			glTexCoord2f(1.0, 0.0)
			glVertex3f(0.0, -1.0, -1.0)
			glTexCoord2f(1.0, 1.0)
			glVertex3f(0.0, -1.0, 1.0)
			glTexCoord2f(0.0, 1.0)
			glVertex3f(0.0, 1.0, 1.0)
			glEnd()

			glPopMatrix()


# =====================================================================================

class Mur(Maillage):

	def __init__(self,**attributs):
		Maillage.__init__(self)
		self.visible = True
		self.hauteur = attributs.get("hauteur",2.5)
		texture = attributs.get('texture',"../data/textures/dante.jpg")
		self.texture = TextureCatalog().loadTexture(texture) 
		self.v = []
		self.parse(attributs.get("points",None))


	def parse(self,points):
		if points != None :
			tokens = points.split(",")
			for unToken in tokens :
				sx,sy = unToken.split()
				x,y   = float(sx), float(sy)
				self.v.append((x,y))

	def draw(self):
		glBindTexture(GL_TEXTURE_2D,self.texture.id)
		h = self.hauteur
		
		for i in range(len(self.v)-1):
			x0, y0 = self.v[i]
			x1, y1 = self.v[i+1]
			glBegin(GL_QUADS)
			glTexCoord2f(0.0, 0.0)
			glVertex3f(x0, y0, 0.0)
			glTexCoord2f(1.0, 0.0)
			glVertex3f(x1, y1, 0.0)
			glTexCoord2f(1.0, 1.0)
			glVertex3f(x1, y1, h)
			glTexCoord2f(0.0, 1.0)
			glVertex3f(x0, y0, h)
			glEnd()

			glBegin(GL_QUADS)
			glTexCoord2f(0.0, 0.0)
			glVertex3f(x1, y1, 0.0)
			glTexCoord2f(1.0, 0.0)
			glVertex3f(x0, y0, 0.0)
			glTexCoord2f(1.0, 1.0)
			glVertex3f(x0, y0, h)
			glTexCoord2f(0.0, 1.0)
			glVertex3f(x1, y1, h)
			glEnd()



# =====================================================================================


class Obj(Maillage):
	def __init__(self,**attributs):
		Maillage.__init__(self)
		self.url = attributs.get("url","../data/obj/pingouin/p.obj")
		self.model = wavefront.WavefrontModel()
		self.model.LoadFile(self.url)

	def draw(self):
		if self.perceptible:
			self.model.Draw()


class ObjY(Maillage):
	def __init__(self,**attributs):
		Maillage.__init__(self)
		self.url = attributs.get("url","../data/obj/pingouin/p.obj")
		self.model = formes.wavefront.WavefrontModel()
		self.model.LoadFile(self.url)

	def draw(self):
		if self.perceptible:
			glPushMatrix()
			glRotatef(90.0,1.0,0.0,0.0)
			self.model.Draw()
			glPopMatrix()

# =====================================================================================

class Sol(Maillage) : 
	def __init__(self,**attributs):
		Maillage.__init__(self)
		self.size   = attributs.get('size',500)
		textureName = attributs.get('texture','../data/textures/moquette.jpg')
		self.texture = TextureCatalog().loadTexture(textureName)
		# self.facteurTexture = getVal(attr,float,"facteurTexture",1.0)
	
	def draw(self):

		#size = self.size
		if self.perceptible:
			size=100
			fz = 1.0
		
			glBindTexture(GL_TEXTURE_2D,self.texture.id)
			glBegin(GL_QUADS)
			glTexCoord2f(0.0,0.0)
			glVertex3f(-size,-size,0.0)
			glTexCoord2f(size,0.0)
			glVertex3f(size,-size,0.0)
			glTexCoord2f(size,size)
			glVertex3f(size,size,0.0)
			glTexCoord2f(0.0,size)
			glVertex3f(-size,size,0.0)
			glEnd()

# =====================================================================================


class Ciel(Maillage):
		def __init__(self,**attributs):
			Maillage.__init__(self)
			self.size = attributs.get('size',500.0)
	
			textureName = attributs.get('texture','../data/skyboxes/ciel.jpg')
			image = pyglet.image.load(textureName)
			imageSeq = pyglet.image.ImageGrid(image, 3, 4)
			self.textureUP = imageSeq[9].get_texture()
			self.textureDN = imageSeq[1].get_texture()
			self.textureLT = imageSeq[4].get_texture()
			self.textureFT = imageSeq[5].get_texture()
			self.textureRT = imageSeq[6].get_texture()
			self.textureBK = imageSeq[7].get_texture()
			self.textureFactor = 1.0	
	
		def draw(self):
				if self.perceptible :
					size = self.size
					halfsize = (size/2)
					halfsizec = halfsize*1.01 #halfsize corrected
					tf = self.textureFactor
		
					glPushMatrix()
					glRotatef(90.0,1.0,0.0,0.0)

					# Up
					glBindTexture(GL_TEXTURE_2D,self.textureUP.id)
					glBegin(GL_QUADS)
					glTexCoord2f(0.0,0.0)
					glVertex3f(-halfsizec,halfsize,-halfsizec)
					glTexCoord2f(1.0,0.0)
					glVertex3f(halfsizec,halfsize,-halfsizec)
					glTexCoord2f(1.0,1.0)
					glVertex3f(halfsizec,halfsize,halfsizec)
					glTexCoord2f(0.0,1.0)
					glVertex3f(-halfsizec,halfsize,halfsizec)
					glEnd()
					# Down
					glBindTexture(GL_TEXTURE_2D,self.textureDN.id)
					glBegin(GL_QUADS)
					glTexCoord2f(0.0,0.0)
					glVertex3f(-halfsizec,-halfsize,halfsizec)
					glTexCoord2f(1.0,0.0)
					glVertex3f(halfsizec,-halfsize,halfsizec)
					glTexCoord2f(1.0,1.0)
					glVertex3f(halfsizec,-halfsize,-halfsizec)
					glTexCoord2f(0.0,1.0)
					glVertex3f(-halfsizec,-halfsize,-halfsizec)
					glEnd()
					# Left
					glBindTexture(GL_TEXTURE_2D,self.textureLT.id)
					glBegin(GL_QUADS)
					glTexCoord2f(0.0,0.0)
					glVertex3f(-halfsize,-halfsizec,halfsizec)
					glTexCoord2f(1.0,0.0)
					glVertex3f(-halfsize,-halfsizec,-halfsizec)
					glTexCoord2f(1.0,1.0)
					glVertex3f(-halfsize,halfsizec,-halfsizec)
					glTexCoord2f(0.0,1.0)
					glVertex3f(-halfsize,halfsizec,halfsizec)
					glEnd()
					# Front
					glBindTexture(GL_TEXTURE_2D,self.textureFT.id)
					glBegin(GL_QUADS)
					glTexCoord2f(0.0,0.0)
					glVertex3f(-halfsizec,-halfsizec,-halfsize)
					glTexCoord2f(1.0,0.0)
					glVertex3f(halfsizec,-halfsizec,-halfsize)
					glTexCoord2f(1.0,1.0)
					glVertex3f(halfsizec,halfsizec,-halfsize)
					glTexCoord2f(0.0,1.0)
					glVertex3f(-halfsizec,halfsizec,-halfsize)
					glEnd()
					# Right
					glBindTexture(GL_TEXTURE_2D,self.textureRT.id)
					glBegin(GL_QUADS)
					glTexCoord2f(0.0,0.0)
					glVertex3f(halfsize,-halfsizec,-halfsizec)
					glTexCoord2f(1.0,0.0)
					glVertex3f(halfsize,-halfsizec,halfsizec)
					glTexCoord2f(1.0,1.0)
					glVertex3f(halfsize,halfsizec,halfsizec)
					glTexCoord2f(0.0,1.0)
					glVertex3f(halfsize,halfsizec,-halfsizec)
					glEnd()
					# Back
					glBindTexture(GL_TEXTURE_2D,self.textureBK.id)
					glBegin(GL_QUADS)
					glTexCoord2f(0.0,0.0)
					glVertex3f(halfsizec,-halfsizec,halfsize)
					glTexCoord2f(1.0,0.0)
					glVertex3f(-halfsizec,-halfsizec,halfsize)
					glTexCoord2f(1.0,1.0)
					glVertex3f(-halfsizec,halfsizec,halfsize)
					glTexCoord2f(0.0,1.0)
					glVertex3f(halfsizec,halfsizec,halfsize)
					glEnd()

					glPopMatrix()
								