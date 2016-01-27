import geo
import visu

import math
import random


class Monde:

    def __init__(self):
        self.horloge = 0.0
        self.camera = visu.Camera()
        self.decor = []
        self.activites = []
        self.annuaire = {}

    def dessiner(self):
        self.camera.lookAt()
        for x in self.decor:
            x.dessiner()

    def actualiser(self, dt):
        self.horloge += dt
        for x in self.activites:
            x.actualiser(self.horloge, dt)

    def ajouter(self, decor=None, activite=None):
        if decor != None:
            self.decor.append(decor)
        if activite != None:
            self.activites.append(activite)

    def enregistrer(self, nom, obj):
        self.annuaire[nom] = obj

    def d(self):
        """
        Retourne la distance entre le pingouin et l'avatar
        """
        return self.camera.repere.o.distance(self.pingouin.repere.o)

    def a(self):
        """
        Retourne l'angle entre la caméra et le pingouin
        """
        vp = geo.Vec3((0.0, 0.0, 0.0))
        vp.moins(self.pingouin.repere.o, self.camera.repere.o)
        camera_angle = self.camera.repere.angle
        va = geo.Vec3((math.cos(camera_angle), math.sin(camera_angle), 0))
        return vp.angleEntre(va)

class Activite:

    def __init__(self, id=None, objet=None):
        self.id = id
        self.actif = False
        self.objet = objet

    def start(self):
        self.actif = True

    def stop(self):
        self.actif = False

    def pause(self):
        self.actif = False

    def actualiser(self, t, dt):
        if self.actif:
            print("ACTIVITE : ", t, " - ", dt)


class Fou(Activite):

    def __init__(self, id=None, objet=None):
        Activite.__init__(self, id, objet)

    def actualiser(self, t, dt):
        if self.objet != None:
            x = random.random()
            if x < 0.4:
                self.objet.avancer(4.0 * dt)
            elif x < 0.6:
                self.objet.tourner(math.pi / 4.0)
            elif x < 0.8:
                self.objet.tourner(-math.pi / 3.0)
            else:
                pass
