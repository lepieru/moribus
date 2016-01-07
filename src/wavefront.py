"""
provides an interface to load and draw Wavefront object files.
created by: Toby de Havilland
edited by: Erwan Martin (public@fzwte.net)
"""

import pyglet
from pyglet.gl import *
#from OpenGL.GLU import *
#from OpenGL.GL import *
import Image
import os.path
import sys
import math

def vec(*args):
	return (GLfloat * len(args))(*args)

image_count=0



class CatalogueTextures : 

	def __init__(self):
		self.catalogue = {}

	def chargerTexture(self,nom):

		if self.catalogue.has_key(nom):
			return self.catalogue[nom]
		else:
			image = pyglet.image.load(nom)
			print ">>>>> TEXTURE ", nom, " CHARGEE"
			texture = image.get_texture()
			glBindTexture(GL_TEXTURE_2D,texture.id)
			glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
			glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
			glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
			self.catalogue[nom] = texture
			return texture

catalogueTextures = CatalogueTextures()




def _nearest_pow2(v):
    # From http://graphics.stanford.edu/~seander/bithacks.html#RoundUpPowerOf2
    # Credit: Sean Anderson
    v -= 1
    v |= v >> 1
    v |= v >> 2
    v |= v >> 4
    v |= v >> 8
    v |= v >> 16
    return v + 1

class Position3D(object):
	def __init__(self, x=0.0, y=-1.5, z=-3.5):
		self.x = x
		self.y = y
		self.z = z

class Rotation3D(object):
	def __init__(self, angle=0.0, x=0.0, y=1.0, z=0.0):
		self.angle = angle
		self.x = x
		self.y = y
		self.z = z

class Material(object):
	def __init__(self):
		self.name = ""
		self.Ka = None
		self.Kd = None
		self.mapKd = ""
		self.Ks = None
		self.Ns = None
		self.Ni = None
		self.dissolve = None
		self.illum = None
		self.textureID = None
		self.texture = None

class face(object):
	def __init__(self):
		self.triIndices = []
		self.materialName = ""

class AbstractModel(object):
	def __init__(self):
		self.position = Position3D()
		self.rotation = Rotation3D()
		self.vertices = []
		self.texCoords = []
		self.normals = []
		self.materials = {}
		self.faces = []
		self.displayListID = None
		self.texture_images={}

	def __del__(self):
		self.FreeResources()

	def FreeResources(self):

		# Delete the display list and textures
		if self.displayListID is not None:
			glDeleteLists(self.displayListID, 1)
			self.displayListID = None

		# Delete any textures we used
		for material in self.materials.itervalues():
			if material.textureID is not None:
				glDeleteTextures(material.textureID)

		# Clear all the materials
		self.materials.clear()

		# Clear the geometry lists
		del self.vertices[:]
		del self.texCoords[:]
		del self.normals[:]
		del self.faces[:]

	def Draw(self):

		vertices = self.vertices
		texCoords = self.texCoords
		normals = self.normals

		glLightfv(GL_LIGHT0,GL_POSITION,vec(0.0,10.0,5.0,1.0))
		glLightfv(GL_LIGHT0,GL_DIFFUSE, vec(1.0,1.0,1.0,1.0))

		# Loop through each group
		for face in self.faces:
			material = self.materials[face.materialName]
		
			# Set color and materials based on group's material
			
			#if material.Ka:
			#	glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, material.Ka)

			#if material.Kd:
			#	glColor4f(material.Kd[0], material.Kd[1],material.Kd[2],1.0)
			#	print material.Kd
			#	glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, material.Kd)

			#if material.Ks:
			#	glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, material.Ks)

			#if material.Ns:
			#	glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, material.Ns)

			if material.texture:
				glEnable(GL_TEXTURE_2D)
				
				glEnable(GL_BLEND) 
				glDisable(GL_COLOR_MATERIAL);
				glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

				
				glBindTexture(GL_TEXTURE_2D,material.texture.id)
			
				
			else:
				glDisable(GL_TEXTURE_2D)

			glBegin(GL_TRIANGLES)
			for vi, ti, ni in face.triIndices:
				if len(texCoords):
					s,t = texCoords[ti]
					glTexCoord2f(s,t)
				if len(normals):
					nx, ny, nz = normals[ni]
					glNormal3f(nx,ny,nz)
				if len(vertices):
					x, y, z = vertices[vi]
					glVertex3f(x,y,z)
			glEnd()

		#glDisableClientState(GL_VERTEX_ARRAY)
		#glDisableClientState(GL_NORMAL_ARRAY)

	def DrawQuick(self):

		glLoadIdentity()
		glRotatef(15, 1, 0, 0)
		glTranslatef(self.position.x, self.position.y, self.position.z)
		glRotatef(self.rotation.angle,self.rotation.x,self.rotation.y,self.rotation.z)

		if self.displayListID is None:
			self.displayListID = glGenLists(1)
			glNewList(self.displayListID, GL_COMPILE)
			self.Draw()
			glEndList()

		glCallList(self.displayListID)

class WavefrontModel(AbstractModel):
	def __init__(self):
		AbstractModel.__init__(self)

	def LoadMTL(self, fileName):

		material = None
		try:
			fileHandle = file(fileName)
		except IOError:
			print "Failed to open MTL file: %s" % fileName
			return
		for line in fileHandle:
			# Parse command and data from each line
			words = line.split()
			if len(words):
				command = words[0]
				data = words[1:]

				if command == 'newmtl':
					material = Material()
					material.name = data[0]
					self.materials[data[0]] = material

				elif command == 'Ka':
					r = float(data[0])
					g = float(data[1])
					b = float(data[2])
					material.Ka = vec(r, g, b)

				elif command == 'Kd':
					r = float(data[0])
					g = float(data[1])
					b = float(data[2])
					material.Kd = vec(r, g, b)

				elif command == 'Ks':
					r = float(data[0])
					g = float(data[1])
					b = float(data[2])
					material.Ks = vec(r, g, b)

				elif command == 'Ns':
					material.Ns = float(data[0])

				elif command == 'Ni':
					material.Ni = float(data[0])

				elif command == 'd':
					material.dissolve = float(data[0])

				elif command == 'illum':
					material.illum = int(data[0])

				elif command == 'map_Kd':
					modelPath = os.path.split(fileName)[0]
					material.mapKd = os.path.join(modelPath, data[0])
					material.texture = catalogueTextures.chargerTexture(material.mapKd)
					if material.texture != None :
						material.textureId = material.texture.id
					

	def LoadFile(self, fileName, scale = 1.0):

		self.FreeResources()

		currentface = None
		fileHandle = file(fileName)
		for line in fileHandle:
			# Parse command and data from each line
			words = line.split()
			if len(words):
				command = words[0]
				data = words[1:]

				if command == 'mtllib': # Material library
					modelPath = os.path.split(fileName)[0]
					mtllibPath = os.path.join(modelPath, data[0])
					self.LoadMTL(mtllibPath)

				elif command == 'v': # Vertex
					x, y, z = data
					vertex = (float(x) * scale, float(y) * scale, float(z) * scale)
					self.vertices.append(vertex)

				elif command == 'vt': # Texture coordinate
					if len(data) == 3:
						s, t, rien = data
					else:
						s, t = data
					texCoord = (float(s), float(t))
					self.texCoords.append(texCoord)

				elif command == 'vn': # Normal
					x, y, z = data
					normal = (float(x) * scale, float(y) * scale, float(z) * scale)
					self.normals.append(normal)

				elif command == 'usemtl' : # Use material
					currentface = face()
					currentface.materialName = data[0]
					self.faces.append(currentface)

				elif command == 'f':

					#if len(data) > 3:
						#print "Sorry, only triangles are supported"
						#print "Please triangulate the model before exporting"
						#sys.exit(1)

					if len(data) == 3:
						# Parse indices from triples
						for word in data:
							bits = word.split('/')
							vi = int(bits[0])-1
							# Make relative negative vert indicies absolute
							if vi < 0:
								vi= len(self.vertices) + vi + 1
							ti=0
							ni=0
							if len(bits) >1 and bits[1]:
								ti = int(bits[1])-1
								# Make relative negative vert indicies absolute
								if ti < 0:
									ti= len(self.texCoords) + ti + 1
							if len(bits) >2 and bits[2]:
								ni = int(bits[2])-1
							indices = (vi, ti, ni)
							currentface.triIndices.append(indices)
							
					if len(data) == 4:
						# Parse indices from triples
						data1 = [data[0],data[1],data[2]]
						for word in data1:
							bits = word.split('/')
							vi = int(bits[0])-1
							# Make relative negative vert indicies absolute
							if vi < 0:
								vi= len(self.vertices) + vi + 1
							ti=0
							ni=0
							if len(bits) >1 and bits[1]:
								ti = int(bits[1])-1
								# Make relative negative vert indicies absolute
								if ti < 0:
									ti= len(self.texCoords) + ti + 1
							if len(bits) >2 and bits[2]:
								ni = int(bits[2])-1
							indices = (vi, ti, ni)
							currentface.triIndices.append(indices)
							
						data2 = [data[2],data[3],data[0]]
						for word in data2:
							bits = word.split('/')
							vi = int(bits[0])-1
							# Make relative negative vert indicies absolute
							if vi < 0:
								vi= len(self.vertices) + vi + 1
							ti=0
							ni=0
							if len(bits) >1 and bits[1]:
								ti = int(bits[1])-1
								# Make relative negative vert indicies absolute
								if ti < 0:
									ti= len(self.texCoords) + ti + 1
							if len(bits) >2 and bits[2]:
								ni = int(bits[2])-1
							indices = (vi, ti, ni)
							currentface.triIndices.append(indices)							

		print "Model loaded"
		print "Number vertices: %d" % len(self.vertices)
		print "Number texCoords: %d" % len(self.texCoords)
		print "Number normals: %d" % len(self.normals)
		print "Number materials: %d" % len(self.materials)
		print "Number faces: %d" % len(self.faces)

if __name__ == "__main__":

	model = WavefrontModel()
	model.LoadFile('models/tank/wall4.obj', 0.5)
