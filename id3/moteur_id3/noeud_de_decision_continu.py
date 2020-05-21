from .noeud_de_decision import NoeudDeDecision

class NoeudDeDecision_continu(NoeudDeDecision):

    def __init__(self, attribut, donnees, p_class, enfants=None, val = None):
        """
            Classe enfant de NoeudDeDecision spécialement prévue pour supporter 
            l'utilisation de données continues. Différentes méthodes ont été redéfinies ici pour 
            ce faire et un attribut utile a été ajouté.

            :param attribut: l'attribut de partitionnement du noeud (``None`` si\
            le noeud est un noeud terminal).
            :param list donnees: la liste des données qui tombent dans la\
            sous-classification du noeud.
            :param enfants: un dictionnaire associant un fils (sous-noeud) à\
            chaque valeur de l'attribut du noeud, comme nous avons affaire à un partitonnement
            binaire, les deux valeurs possibles après partitionnement sont "NoeudGauche" (valeur inférieure à la valeur 
            de partitionnement) ou "NoeudDroit" (valeur supérieure ou égale à la valeur de partitionnement)
            :param p_class : classe prépondérante dans les données du noeud
            :param valeur_de_partitionnement : Valeur choisie pour son entropie minimale permettant la séparation
            des données entre les deux noeuds enfants
        """
        #Appel du constructeur de NoeudDeDecision
        NoeudDeDecision.__init__(self, attribut, donnees, p_class, enfants)

        self.valeur_de_partitionnement = val    

    #Surcharges des méthodes devant être adaptées pour ID3_continu :    

    def classifie(self, donnee, print = True):
        """ Classifie une donnée à valeurs continues à l'aide de l'arbre de décision généré par ID3_continu
            :param donnee: la donnée à classifier, dictionnaire de forme {attribut:valeur}
            :return: la classe de la donnée selon le noeud de décision courant.
        """
        rep = ''

        if self.terminal():
            rep += 'Alors {}'.format(self.classe().upper())
        else:         
            valeur = float(donnee[self.attribut])
            rep += 'Si ' + self.attribut 

            if valeur < self.valeur_de_partitionnement:
                enfant = self.enfants["NoeudGauche"]
                rep += ' < '
            elif valeur >= self.valeur_de_partitionnement:
                enfant = self.enfants["NoeudDroit"]
                rep += ' >= '

            rep += str(self.valeur_de_partitionnement) + '\n'

            try:
                rep += enfant.classifie(donnee)
            except:
                rep += self.p_class
        
        if print == True:
            return rep
        else:
            return str(float(rep[-3]))

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
