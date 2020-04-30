from math import log
from .noeud_de_decision import NoeudDeDecision

class ID3:
    """ Algorithme ID3. """
    
    def construit_arbre(self, donnees):
        """ Construit un arbre de décision à partir des données d'apprentissage.

            :param list donnees: les données d'apprentissage\
            ``[classe, {attribut -> valeur}, ...]``.
            :return: une instance de NoeudDeDecision correspondant à la racine de\
            l'arbre de décision.
        """
        
        # Nous devons extraire les domaines de valeur des 
        # attributs, puisqu'ils sont nécessaires pour 
        # construire l'arbre.
        attributs = {}
        for donnee in donnees:
            for attribut, valeur in donnee[1].items():
                valeurs = attributs.get(attribut)
                if valeurs is None:
                    valeurs = set()
                    attributs[attribut] = valeurs
                valeurs.add(valeur)
            
        arbre = self.construit_arbre_recur(donnees, attributs)
        
        return arbre

    def construit_arbre_recur(self, donnees, attributs):
        """ Construit rédurcivement un arbre de décision à partir 
            des données d'apprentissage et d'un dictionnaire liant
            les attributs à la liste de leurs valeurs possibles.

            :param list donnees: les données d'apprentissage\
            ``[classe, {attribut -> valeur}, ...]``.
            :param attributs: un dictionnaire qui associe chaque\
            attribut A à son domaine de valeurs a_j.
            :return: une instance de NoeudDeDecision correspondant à la racine de\
            l'arbre de décision.
        """
        
        print('à compléter')

    def partitionne(self, donnees, attribut, valeurs):
        """ Partitionne les données sur les valeurs a_j de l'attribut A.

            :param list donnees: les données à partitioner.
            :param attribut: l'attribut A de partitionnement.
            :param list valeurs: les valeurs a_j de l'attribut A.
            :return: un dictionnaire qui associe à chaque valeur a_j de\
            l'attribut A une liste l_j contenant les données pour lesquelles A\
            vaut a_j.
        """
        partitions = {}

        for val in valeurs:
            partitions[val] = []

        for donnee in donnees:
            
            partition = partitions[donnee[1][attribut]]
            partition.append(donnee)

        return partitions

    def p_aj(self, donnees, attribut, valeur):
        """ p(a_j) - la probabilité que la valeur de l'attribut A soit a_j.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param valeur: la valeur a_j de l'attribut A.            
            :return: p(a_j)
        """

        if len(donnees) == 0:
            return 0.0
            
        nbr_occurences = 0

        for donnee in donnees:
            if donnee[1][attribut] == valeur :
                nbr_occurences += 1
        
        return nbr_occurences/len(donnees)

    def p_ci_aj(self, donnees, attribut, valeur, classe):
        """ p(c_i|a_j) - la probabilité conditionnelle que la classe C soit c_i\
            étant donné que l'attribut A vaut a_j.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param valeur: la valeur a_j de l'attribut A.
            :param classe: la valeur c_i de la classe C.
            :return: p(c_i | a_j)
        """
        nbr_donnees_avec_aj = 0
        nbr_donnees_avec_aj_ci = 0

        for donnee in donnees:
            if donnee[1][attribut] == valeur:
                nbr_donnees_avec_aj += 1

                if donnee[0] == classe:
                    nbr_donnees_avec_aj_ci += 1
        
        if nbr_donnees_avec_aj_ci == 0:
            return 0
                
        return nbr_donnees_avec_aj_ci/nbr_donnees_avec_aj    
        


    def h_C_aj(self, donnees, attribut, valeur):
        """ H(C|a_j) - l'entropie de la classe parmi les données pour lesquelles\
            l'attribut A vaut a_j.

            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param valeur: la valeur a_j de l'attribut A.
            :return: H(C|a_j)
        """
        classes = []
        for donnee in donnees:
            if donnee[0] not in classes:
                classes.append(donnee[0])

        proba_ci_aj = []

        for classe in classes:
            proba_ci_aj.append(self.p_ci_aj(donnees, attribut, valeur, classe))

        entropie = 0

        for proba in proba_ci_aj:
            if proba !=0:
                entropie -= proba*log(proba,2.0)

        return entropie

    def h_C_A(self, donnees, attribut, valeurs):
        """ H(C|A) - l'entropie de la classe après avoir choisi de partitionner\
            les données suivant les valeurs de l'attribut A.
            
            :param list donnees: les données d'apprentissage.
            :param attribut: l'attribut A.
            :param list valeurs: les valeurs a_j de l'attribut A.
            :return: H(C|A)
        """
        proba_aj = []
        entropie_c_aj = []

        for val in valeurs:
            proba_aj.append(self.p_aj(donnees, attribut, val))
            entropie_c_aj.append(self.h_C_aj(donnees, attribut, val))
        
        somme = 0

        for i in range(len(proba_aj)):
            somme += proba_aj[i]*entropie_c_aj[i]

        return somme