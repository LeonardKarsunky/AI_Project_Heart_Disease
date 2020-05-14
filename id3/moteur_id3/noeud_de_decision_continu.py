from .noeud_de_decision import NoeudDeDecision

class NoeudDeDecision_continu(NoeudDeDecision):
    def __init__(self, attribut, donnees, p_class, enfants=None, val = None):
        
        NoeudDeDecision.__init__(self, attribut, donnees, p_class, enfants)
        self.valeur_de_partitionnement = val

    def classifie(self, donnee, print = True):
        """ Classifie une donnée à valeurs continues à l'aide de l'arbre de décision généré par ID3_continu
            :param donnee: la donnée à classifier.
            :return: la classe de la donnée selon le noeud de décision courant.
        """
        classe = None

        rep = ''
        if self.terminal():
            rep += 'Alors {}'.format(self.classe().upper())
            classe = self.classe()
        else:         
            valeur = float(donnee[self.attribut])
            rep += 'Si ' + self.attribut 

            if valeur < self.valeur_de_partitionnement:
                enfant = self.enfants["NoeudGauche"]
                rep += ' < '
            else:
                enfant = self.enfants["NoeudDroit"]
                rep += ' >= '

            rep += str(self.valeur_de_partitionnement)

            try:
                rep += enfant.classifie_continu(donnee)
            except:
                rep += self.p_class
        
        if print == True:
            return rep
        else:
            return classe

    def repr_arbre(self, level=0):
        """ Représentation sous forme de string de l'arbre de décision duquel\
            le noeud courant est la racine. 
        """

        rep = ''
        if self.terminal():
            rep += '---'*level
            rep += 'Alors {}\n'.format(self.classe().upper())
            rep += '---'*level + '\n'

        else:
            for cote, enfant in self.enfants.items():

                rep += '---'*level
                rep += 'Si ' + str(self.attribut)
                if cote == "NoeudGauche":
                    rep += ' < '
                elif cote == "NoeudDroit":
                    rep += ' >= '
                
                rep += str(self.valeur_de_partitionnement)
                rep += '\n'
                rep += enfant.repr_arbre(level+1)

        return rep

    def __repr__(self):
        """ Représentation sous forme de string de l'arbre de décision duquel\
            le noeud courant est la racine. 
        """

        return str(self.repr_arbre(level=0))