import vec3


class Noeud : 

	def __init__(self,v,coutMax=10000.0):
		self.v = v
		self.pred = None
		self.cout = coutMax
		self.marque = False

	def valeur(self):
		return self.v

class Graphe : 
	def __init__(self,oriente=True):
		self.sucs = {}
		self.sommets = {}
		self.oriente = oriente
		
	def coordonnees(self,l):
		return [self.etiquette(s) for s in l]

	def ajouterSommet(self,nom,v):
		self.sommets[nom] = Noeud(v)
		self.sucs[nom] = {}

	def ajouterArc(self,ori,ext,v=100000.0):
		sucs = self.sucs[ori]
		sucs[ext] = v
		if self.oriente == False :
			sucs = self.sucs[ext]
			sucs[ori] = v

	def premierSommet(self):
		l = self.sommets.keys()
		if len(l) == 0 :
			return None
		else:
			return l[0]

	def dernierSommet(self):
		l = self.sommets.keys()
		if len(l) == 0 :
			return None
		else:
			return l[-1]

	def successeurs(self,s): 
		sucs = self.sucs[s]
		return sucs.keys()

	def etiquette(self,nom):
		x = self.sommets[nom]
		return x.v

	def coutArc(self, ori,ext):
		sucs = self.sucs[ori]
		return sucs[ext]

	def setCoutArc(self,ori,ext,v):
		sucs = self.sucs[ori]
		sucs[ext] = v
		if self.oriente == False :
			sucs = self.sucs[ext]
			sucs[ori] = v










def cmpCout(v1,v2):
	n1, c1 = v1
	n2, c2 = v2
	if c1 < c2 : return -1 
        elif c1 > c2 : return 1
        else: return 0 

class Dijkstra :

	def __init__(self,g,coutMax=100000.0):
		self.graphe = g
		self.E = {}
		self.coutMax = coutMax

	def trouverChemin(self,de=None,a=None):
		return self.graphe.coordonnees(self.chercher(de,a))

	def chercher(self, ori, ext):

		# print "Pour aller de ", ori, " a ", ext
		
		n = len(self.graphe.sommets)

		# print "Nombre de sommets : ", n
		
		n_ori = self.graphe.sommets[ori]
		n_ori.cout = 0.0 

		# Initialisation
		# --------------

		graphe = self.graphe
		sommets = self.graphe.sommets

		for nom in sommets :
			noeud = sommets[nom]			 
			noeud.cout = self.coutMax
			noeud.pred = None
			noeud.marque = False

		n_ori = sommets[ori]
		n_ori.cout = 0.0
		n_ori.marque = True
		
		encore = True

		# print sommets
		

		s0 = ori
		while encore : 

			# Mise a jour des successeurs du sommet courant
			c0 = sommets[s0].cout
			sucs = graphe.successeurs(s0)
			# print "Sommet courant : ", s0
			for e in sucs :
				n_ext = sommets[e]
				if n_ext.marque == False :
					# print "Examen de ", e
					cout_ext = c0 + graphe.coutArc(s0,e)
					if cout_ext < n_ext.cout:
						# print "Mise a jour de ", e
						n_ext.cout = cout_ext
						n_ext.pred = s0
			l = [(nom,sommets[nom].cout) for nom in sommets if sommets[nom].marque==False]
			l.sort(cmpCout)
			# print l

			# Selection du prochain sommet courant
			# nom,cout = l[0]
			# sommets[nom].marque = True
			# s0 = nom
 
			if len(l)>0 : 
				x = l[0]
				# print ">> ", x[0]
				sommets[x[0]].marque = True
				s0 = x[0]
			else:
				encore = False
			n = n-1
			encore = (n > 0) 

		# Reconstituer le chemin

		chemin = []
		# print "Pour aller de ", ori, " a ", ext
		s0 = ext
		while s0 != None : 
			chemin.append(s0)
			s0 = sommets[s0].pred
		chemin.reverse()
		return chemin

		
		
	

def lireGrapheNavigation(nomFichier):
	gr = Graphe(oriente=False)
	f = open(nomFichier,"r")

	for ligne in f :
		mots = ligne.split()
		if len(mots) > 0 :
			if mots[0]=='#':
				pass
			elif mots[0]=='s':
				nom = mots[1]
				x = float(mots[3])
				y = float(mots[4])
				z = float(mots[5])
				gr.ajouterSommet(nom,vec3.Vec3((x,y,z)))
			elif mots[0] == 'a':
				ori = mots[1]
				ext = mots[2]
				p1 = gr.etiquette(ori)
				p2 = gr.etiquette(ext)
				dist = p1.distance(p2)
				gr.ajouterArc(ori,ext,dist)

	f.close()

	return gr
	
class Navigateur(Dijkstra) : 
  def __init__(self,nomFichier):
    Dijkstra.__init__(self,lireGrapheNavigation(nomFichier))



if __name__ == "__main__":

	import vec3 

	unGraphe = lireGrapheNavigation("graphe.nav")
	dij = Dijkstra(unGraphe)
	print unGraphe.coordonnees(dij.chercher("p0","p3"))
	print dij.trouverChemin(de="p0",a="p3")

	print unGraphe


	
