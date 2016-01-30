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
        self.calculerD()
        self.calculerA()
        # self.calculerACam()
        self.calculerV()
        if not hasattr(self, "activiteCourante"):
            self.changeActivite("pose")
        self.annuaire[self.activiteCourante].actualiser(self.horloge, dt)
        self.afficherEtat()
        self.changeActivitePeutEtre()

    def afficherEtat(self):
        print("Activite courante:       ", self.activiteCourante)
        print("Activite courante depuis: %.1f" % self.activiteDepuis())
        print("(d) Distance:            ", round(self.d), "metre(s)")
        print("(a) Angle:               ", round(self.a * 180 / math.pi), "degre(s)")
        print("(v) Vitesse:             ", round(self.v), "km/h")
        print("------------------------")

    def ajouter(self, decor=None, activite=None):
        if decor != None:
            self.decor.append(decor)
        if activite != None:
            self.activites.append(activite)
            self.enregistrer(activite.id, activite)

    def enregistrer(self, nom, obj):
        self.annuaire[nom] = obj

    def changeActivite(self, activiteId):
        if hasattr(self, "activiteCourante"):
            self.annuaire[self.activiteCourante].stop()
        self.activiteCourante = activiteId
        self.dernierChangementActivite = self.horloge
        self.annuaire[activiteId].start()

    def activiteDepuis(self):
        return self.horloge - self.dernierChangementActivite

    def changeActivitePeutEtre(self):
        self.annuaire[self.activiteCourante].changePeutEtre()

    def calculerD(self):
        """
        Calcul la distance entre le pingouin et l'avatar
        """
        self.d = self.camera.repere.o.distance(self.pingouin.repere.o)

    def calculerACam(self):
        """
        Calcul l'angle entre le pingouin et la camera de l'avatar
        """
        vp = geo.Vec3((0.0, 0.0, 0.0))
        vp.moins(self.pingouin.repere.o, self.camera.repere.o)
        camera_angle = self.camera.repere.angle
        va = geo.Vec3((math.cos(camera_angle), math.sin(camera_angle), 0.0))
        self.aCam = va.angleEntre(vp)

    def calculerA(self):
        """
        Calcul l'angle entre le pingouin et l'avatar
        """
        xp, yp, zp = self.pingouin.repere.o.getCoordonnees()
        xc, yc, zc = self.camera.repere.o.getCoordonnees()
        self.a = math.atan2(yc - yp, xc - xp)

    def calculerV(self):
        """
        Calcul la vitesse de l'avatar
        """
        if not hasattr(self, "anciennePosition"):
            self.anciennePosition = geo.Vec3((0.0, 0.0, 0.0))
            self.anciennePosition.copier(self.camera.repere.o)
        self.v = self.camera.repere.o.distance(self.anciennePosition) * 20
        self.anciennePosition.copier(self.camera.repere.o)


class Activite:

    def __init__(self, id=None, objet=None, monde=None):
        self.id = id
        self.actif = False
        self.objet = objet
        self.monde = monde

    def start(self):
        self.actif = True

    def stop(self):
        self.actif = False

    def pause(self):
        self.actif = False

    def actualiser(self, t, dt):
        pass

    def changePeutEtre(self):
        pass


class Effaye(Activite):

    def actualiser(self, t, dt):
        if self.actif:
            angle = self.monde.a + math.pi
            self.objet.repere.orienter(angle)
            self.objet.avancer(0.1)

    def start(self):
        self.objet.maillage = visu.Obj(url="data/avatars/vert.obj")
        Activite.start(self)

    def changePeutEtre(self):
        if self.monde.d > 15:
            self.monde.changeActivite('pose')


class Aggressif(Activite):

    def actualiser(self, t, dt):
        if self.actif:
            if self.monde.d > 2.2:
                angle = self.monde.a
                self.objet.repere.orienter(angle)
                self.objet.avancer(0.1)
            else:
                x = random.random()
                if x < 0.4:
                    self.objet.avancer(4.0 * dt)
                elif x < 0.6:
                    self.objet.tourner(math.pi / 4.0)
                elif x < 0.8:
                    self.objet.tourner(-math.pi / 3.0)

    def start(self):
        self.objet.maillage = visu.Obj(url="data/avatars/rouge.obj")
        Activite.start(self)

    def changePeutEtre(self):
        if self.monde.d > 4:
            if self.monde.activiteDepuis() > 10:
                self.monde.changeActivite('pose')
            elif self.monde.d > 15:
                self.monde.changeActivite('pose')


class Curieux(Activite):

    def actualiser(self, t, dt):
        if self.actif:
            angle = self.monde.a
            self.objet.repere.orienter(angle)
            if self.monde.d > 5:
                self.objet.avancer(0.05)

    def start(self):
        self.objet.maillage = visu.Obj(url="data/avatars/bleu.obj")
        Activite.start(self)

    def changePeutEtre(self):
        if self.monde.activiteDepuis() > 15:
            self.monde.changeActivite('pose')
        elif self.monde.d < 2:
            if random.random() < 0.5:
                self.monde.changeActivite('aggressif')
            else:
                self.monde.changeActivite('effraye')

class Pose(Activite):

    def actualiser(self, t, dt):
        if self.actif:
            if self.monde.d < 4:
                self.eloigne()
            else:
                if random.random() < 0.01:
                    self.tourne()

    def eloigne(self):
        angle = self.monde.a + math.pi
        self.objet.repere.orienter(angle)
        self.objet.avancer(0.1)

    def tourne(self):
        angle = random.random() * math.pi * 2
        self.objet.repere.orienter(angle)

    def start(self):
        self.objet.maillage = visu.Obj(url="data/obj/pingouin/p.obj")
        Activite.start(self)

    def changePeutEtre(self):
        if self.monde.activiteDepuis() > 1:
            if self.monde.d < 3:
                if random.random() < 0.5:
                    self.monde.changeActivite('aggressif')
                else:
                    self.monde.changeActivite('effraye')
            elif self.monde.d > 20:
                self.monde.changeActivite('curieux')
