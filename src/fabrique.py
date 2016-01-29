import math
import geo
import visu
import simu


class Fabrique:

    def __init__(self, le_monde):
        self.monde = le_monde

    def fabriquer(self):
        sol = visu.Objet(maillage=visu.Sol())

        arbre = visu.Objet(maillage=visu.Panneau(recto="data/textures/tree1.png",
                                                 verso="data/textures/tree1.png",
                                                 largeur=6.0, hauteur=12.0, epaisseur=0.1))
        arbre.placer(geo.Vec3((5.0, 5.0, 0.0)))

        pingouin = visu.Objet(maillage=visu.Obj(url="data/obj/pingouin/p.obj"))
        pingouin.placer(geo.Vec3((-1.0, 0.0, 0.0)))
        pingouin.orienter(45.0 * math.pi / 180.0)

        activite_effraye = simu.Effaye(id="effraye", objet=pingouin, monde=self.monde)
        activite_aggressif = simu.Aggressif(id="aggressif", objet=pingouin, monde=self.monde)
        activite_curieux = simu.Curieux(id="curieux", objet=pingouin, monde=self.monde)
        activite_pose = simu.Pose(id="pose", objet=pingouin, monde=self.monde)

        self.monde.ajouter(decor=sol)
        self.monde.ajouter(decor=arbre)
        self.monde.ajouter(decor=pingouin)

        self.monde.ajouter(activite=activite_effraye)
        self.monde.ajouter(activite=activite_aggressif)
        self.monde.ajouter(activite=activite_curieux)
        self.monde.ajouter(activite=activite_pose)

        self.monde.pingouin = pingouin
