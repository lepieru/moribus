import math
import geo
import visu
import simu


class Fabrique:

    def __init__(self, le_monde):
        self.monde = le_monde

    def fabriquer(self):
        le_sol = visu.Objet(maillage=visu.Sol())
        self.monde.ajouter(decor=le_sol)

        le_tableau = visu.Objet(maillage=visu.Tableau(recto="data/textures/gris.jpg",
                                                      verso="data/textures/Ceramic.jpg",
                                                      largeur=2.0, hauteur=3.0, epaisseur=0.1))
        le_tableau.placer(geo.Vec3((0.0, 0.0, 2.0)))
        self.monde.ajouter(decor=le_tableau)

        le_tableau = visu.Objet(maillage=visu.Panneau(recto="data/textures/tree1.png",
                                                      verso="data/textures/tree1.png",
                                                      largeur=6.0, hauteur=12.0, epaisseur=0.1))
        le_tableau.placer(geo.Vec3((5.0, 5.0, 0.0)))
        self.monde.ajouter(decor=le_tableau)

        le_pingouin = visu.Objet(maillage=visu.Obj(
            url="data/obj/pingouin/p.obj"))
        le_pingouin.placer(geo.Vec3((-2.0, 3.0, 0.0)))
        le_pingouin.orienter(45.0 * math.pi / 180.0)
        self.monde.ajouter(decor=le_pingouin)

        une_activite = simu.Activite(id="act-01")
        # une_activite.start()
        self.monde.ajouter(activite=une_activite)

        une_activite = simu.Fou(id="act-02", objet=le_pingouin)
        une_activite.start()
        self.monde.ajouter(activite=une_activite)
