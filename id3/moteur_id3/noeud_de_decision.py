import statistics

class NoeudDeDecision:
    """ Un noeud dans un arbre de décision. 
    
        This is an updated version from the one in the book (Intelligence Artificielle par la pratique).
        Specifically, if we can not classify a data point, we return the predominant class (see lines 53 - 56). 
    """

    def __init__(self, attribut, donnees, p_class, enfants=None):
        """
            :param attribut: l'attribut de partitionnement du noeud (``None`` si\
            le noeud est un noeud terminal).
            :param list donnees: la liste des données qui tombent dans la\
            sous-classification du noeud.
            :param enfants: un dictionnaire associant un fils (sous-noeud) à\
            chaque valeur de l'attribut du noeud (``None`` si le\
            noeud est terminal).
        """

        self.attribut = attribut
        self.donnees = donnees
        self.enfants = enfants
        self.p_class = p_class
        #utilisé pour la méthode tree_analysis
        self.depth = 0
        #utilisés pour la méthode visual_tree de Results_values
        self.nom = None             #contient un string de forme : attributPère_valeur___nombreUnique
        self.texte = None           #contient un string de forme : attributPère = valeur
        self.parent = None          #contient le noeudDeDecision parent
        self.risques = None         #contient un string valant "Risques faibles" si la classe est 0 et "Risques élevés" si la classe est 1

    def terminal(self):
        """ Vérifie si le noeud courant est terminal. """

        return self.enfants is None

    def classe(self):
        """ Si le noeud est terminal, retourne la classe des données qui\
            tombent dans la sous-classification (dans ce cas, toutes les\
            données font partie de la même classe. 
        """

        if self.terminal():
            return self.donnees[0][0]

    def classifie(self, donnee, print = True):
        """ Classifie une donnée à l'aide de l'arbre de décision duquel le noeud\
            courant est la racine.

            :param donnee: la donnée à classifier.
            :return: la classe de la donnée selon le noeud de décision courant.
        """
        classe = None

        rep = ''
        if self.terminal():
            rep += 'Alors {}'.format(self.classe().upper())
            classe = self.classe()
        else:
            valeur = donnee[self.attribut]
            enfant = self.enfants[valeur]
            rep += 'Si {} = {}, '.format(self.attribut, valeur.upper())
            try:
                rep += enfant.classifie(donnee)
            except:
                rep += self.p_class
        
        if print == True:
            return rep
        else:
            return classe

    def tree_analysis(self):
        """Trouve la profondeur maximale atteinte par par l'arbre lorsque la fonction 
        est appelée sur le noeud racine et initialise l'argument self.depth pour chaque noeud
        pour une éventuelle réutilisation"""

        #liste contenant le niveau de chaque noeud
        niveaux = [0]
        #liste contenant le nombre d'enfants de chaque noeud sauf terminal
        nbr_enfants = []
        #liste des neours pas encore explorés
        noeuds_à_explorer = []
        #Nombe de noeuds terminaux
        nbr_noeuds_terminaux = 0
        #Nombres de noeuds totaux:
        nbr_noeuds = 1

        #Si le noeud racine n'a pas d'enfants, on ne peut pas réaliser d'analyses
        if self.enfants == None:
            return "Erreur"

        #ajoute les enfants du noeud racine aux noeuds à explorer
        for valeur, enfant in self.enfants.items():
            noeuds_à_explorer.append(enfant)
            enfant.depth = 1
            niveaux.append(1)

        #Et le nombre d'enfants du noeud racine à nbr_enfants
        nbr_enfants.append(len(self.enfants))

        #Tant qu'on a pas exploré tous les noeuds
        while noeuds_à_explorer:
            noeud_courant = noeuds_à_explorer.pop(-1)
            niveaux.append(noeud_courant.depth)
            nbr_noeuds += 1

            if noeud_courant.enfants != None:
                nbr_enfants.append(len(noeud_courant.enfants))

                #Si le noeud courant a des enfants, on les rajoute aux noeuds à explorer et on initialise la profondeur de chaque noeud
                for valeur, enfant in noeud_courant.enfants.items():
                    noeuds_à_explorer.append(enfant)
                    enfant.depth = 1 + noeud_courant.depth
            else:
                nbr_noeuds_terminaux += 1                    

        réponse = "La profondeur maximale de l'arbre est : " + str(max(niveaux)) + '\n'
        réponse += "La profondeur moyenne de l'arbre est : " + str(statistics.mean(niveaux)) + '\n'
        réponse += "Le nombre moyen d'enfants tout noeud confondu (sauf noeud terminaux) de l'arbre est : " + str(statistics.mean(nbr_enfants)) + '\n'
        réponse += "Le nombre de noeuds terminaux ou feuilles de cet arbre est : " + str(nbr_noeuds_terminaux) + '\n'
        réponse += "Le nombre de noeuds totaux est : " + str(nbr_noeuds)
        return réponse    

    def repr_arbre(self, level=0):
        """ Représentation sous forme de string de l'arbre de décision duquel\
            le noeud courant est la racine. 
        """

        rep = ''
        if self.terminal():
            rep += '---'*level
            rep += 'Alors {}\n'.format(self.classe().upper())
            rep += '---'*level + '\n'

            """
            rep += 'Décision basée sur les données:\n'
            for donnee in self.donnees:
                rep += '---'*level
                rep += str(donnee) + '\n' 
            """

        else:
            for valeur, enfant in self.enfants.items():
                rep += '---'*level
                rep += 'Si {} = {}: \n'.format(self.attribut, valeur.upper())
                rep += enfant.repr_arbre(level+1)

        return rep

    def __repr__(self):
        """ Représentation sous forme de string de l'arbre de décision duquel\
            le noeud courant est la racine. 
        """

        return str(self.repr_arbre(level=0))