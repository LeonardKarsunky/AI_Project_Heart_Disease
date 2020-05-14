from math import log
from .noeud_de_decision_continu import NoeudDeDecision_continu
import random, math

class ID3_continu:
    """ Algorithme ID3. 

        This is an updated version from the one in the book (Intelligence Artificielle par la pratique).
        Specifically, in construit_arbre_recur(), if donnees == [] (line 70), it returns a terminal node with the predominant class of the dataset -- as computed in construit_arbre() -- instead of returning None.
        Moreover, the predominant class is also passed as a parameter to NoeudDeDecision_continu().
    """
    
    def construit_arbre(self, donnees):
        """ Construit un arbre de décision à partir des données d'apprentissage.

            :param list donnees: les données d'apprentissage\
            ``[classe, {attribut -> valeur}, ...]``.
            :return: une instance de NoeudDeDecision_continu correspondant à la racine de\
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

        # Find the predominant class
        classes = set([row[0] for row in donnees])
        # print(classes)
        predominant_class_counter = -1
        for c in classes:
            # print([row[0] for row in donnees].count(c))
            if [row[0] for row in donnees].count(c) >= predominant_class_counter:
                predominant_class_counter = [row[0] for row in donnees].count(c)
                predominant_class = c
        # print(predominant_class)
            
        arbre = self.construit_arbre_recur(donnees, attributs, predominant_class)

        return arbre

    def construit_arbre_recur(self, donnees, attributs, predominant_class):
        """ Construit rédurcivement un arbre de décision à partir 
            des données d'apprentissage et d'un dictionnaire liant
            les attributs à la liste de leurs valeurs possibles.

            :param list donnees: les données d'apprentissage\
            ``[classe, {attribut -> valeur}, ...]``.
            :param attributs: un dictionnaire qui associe chaque\
            attribut A à son domaine de valeurs a_j.
            :return: une instance de NoeudDeDecision_continu correspondant à la racine de\
            l'arbre de décision.
        """
        
        if donnees == []:
            return NoeudDeDecision_continu(None, [str(predominant_class), dict()], str(predominant_class))

        # Toutes les données restants font parties de la même classe, Noeud terminal        
        elif self.classe_unique(donnees):
            return NoeudDeDecision_continu(None, donnees, str(predominant_class))
            
            # Sélectionne l'attribut et la valeur qui minimise l'entropie
        else:
            attr_et_val = self.attribut_valeur_min_entropie(donnees, attributs)
            attribut = attr_et_val[0]
            valeur = attr_et_val[1]
            
            # Crée les sous-arbres de manière récursive.)
    
            partitions = self.partitionne_binaire(donnees, attribut, valeur)

            part = []
            for donnee in partitions["NoeudDroit"]:
                part.append(donnee[1][attribut])            
            
            enfants = {}

            #L'enfant gauche possède toutes les données dont l'attribut de partitionnement a une valeur inférieure à la valeur de partitionnement
            enfants["NoeudGauche"] = self.construit_arbre_recur(partitions["NoeudGauche"], attributs, predominant_class)
            #L'enfant droit possède toutes les données dont l'attribut de partitionnement a une valeur supérieure à la valeur de partitionnement             
            enfants["NoeudDroit"] = self.construit_arbre_recur(partitions["NoeudDroit"], attributs, predominant_class)
            
            return NoeudDeDecision_continu(attribut, donnees, str(predominant_class), enfants, valeur)

    def classe_unique(self, donnees):
            """ Vérifie que toutes les données appartiennent à la même classe. """
            
            if len(donnees) == 0:
                return True 
            premiere_classe = donnees[0][0]
            for donnee in donnees:
                if donnee[0] != premiere_classe:
                    return False 
            return True
            
    def partitionne_binaire(self, donnees, attribut, valeur_limite):
        """ Partitionne les données en les séparant de façon binaire avec d'un côté les
        données dont la valeur de l'attribut spécifié est inférieure à la valeur_limite et de 
        l'autre les données dont la valeur de l'attribut est supérieure à la valeur limite

            :param list donnees: les données à partitioner.
            :param attribut: l'attribut A de partitionnement.
            :param valeur_limite: la valeur au niveau de laquelle on coupe le jeu de données en deux
            :return: un dictionnaire qui spécifie les deux sets de données obtenus
        """
        partitions = {}
        #L'enfant gauche possède toutes les données dont l'attribut de partitionnement a une valeur inférieure à la valeur de partitionnement
        partitions["NoeudGauche"] = []
        #L'enfant droit possède toutes les données dont l'attribut de partitionnement a une valeur supérieure à la valeur de partitionnement 
        partitions["NoeudDroit"] = []
        
        for donnee in donnees:
            if float(donnee[1][attribut]) < valeur_limite:
                partitions["NoeudGauche"].append(donnee)
            elif float(donnee[1][attribut]) >= valeur_limite:
                partitions["NoeudDroit"].append(donnee)
                
            
        return partitions
    
    def attribut_valeur_min_entropie(self, donnees, attributs):
        """Cherche parmi tous les attributs et toutes leurs valeurs, l'attribut et la valeur minimisant l'entropie
        Et retourne cet attribut et sa valeur de partitionnement correspondante sous forme d'une liste [attribut, valeur]"""
        
        if len(donnees) == 0:
            return "Erreur les données spécifiées sont vides"

        #Dico de forme {attribut:[valeur_de_partitionnment_minimisant_l'entropie, entropie correspondante]}
        dico_attribut_entropie = {}

        #Remplit le dictionnaire
        for attribut in attributs:
            dico_attribut_entropie[attribut] = self.valeur_min_entropie(donnees, attribut)

        entropie_min = 99999.9
        valeur_de_partitionnement = -1.0
        attribut_de_partitionnement = ""

        #Recherche l'attribut associé à une valeur de partitionnement optimale qui minimise le mieux l'entropie
        for attribut, val_et_entropie in dico_attribut_entropie.items():
            entropie_courante = val_et_entropie[1]
            if entropie_courante < entropie_min:
                entropie_min = entropie_courante
                valeur_de_partitionnement = val_et_entropie[0]
                attribut_de_partitionnement = attribut
        
        return [attribut_de_partitionnement, valeur_de_partitionnement]

    def valeur_min_entropie(self, donnees, attribut):
        """ Cherche pour l'attribut spécifié, la valeur qui une fois choisie pour partitionner les données en
            deux sous-ensembles, minimiserait l'entropie et retourne une liste contenant [valeur_minimisant_entropie, entropie_correspondante]
        """
        if len(donnees) == 0 or attribut not in donnees[0][1]:
            return "Erreur les donnees spécifiées sont vides ou incompatibles avec l'attribut spécifié"

        #Trie toutes les valeurs apparaissant dans le set de données de l'attribut spécifié par ordre croissant
        valeurs_triées = self.valeurs_triées(donnees, attribut)
        #On enlève la première valeur car la choisir comme valeur de partitionnement résulterait à avoir un noeud enfant gauche vide
        del valeurs_triées[0]
        #Valeur de partitionnement finale 
        valeur_finale = 0.0
        #Entropie minimale à chaque itération
        entropie_min = 99999.9

        #Recherche de la valeur minimisant l'entropie et de la valeur correspondante
        for valeur in valeurs_triées:
    
            entropie_temp = float(self.entropie_part_binaire(donnees, attribut, valeur))
            if entropie_temp < entropie_min:
                entropie_min = entropie_temp
                valeur_finale = valeur
        
        return [valeur_finale, entropie_min]                     

    def entropie_part_binaire(self, donnees, attribut, valeur_limite):
        """Retourne pour un set de données, un attribut spécifique et une valeur de partionnement pour l'attribut, 
        l'entropie totale (somme de l'entropie des deux sous-ensembles résultants) """

        #On commence par partitionner de façon binaire les donnees en fonction de la valeur_limite spécifiée
        partitions = self.partitionne_binaire(donnees, attribut, valeur_limite)
        nbr_donnees_gauche = len(partitions["NoeudGauche"])
        nbr_donnees_droit = len(partitions["NoeudDroit"])
        nbr_donnees_total = len(donnees)

        proba_gauche = nbr_donnees_gauche/nbr_donnees_total
        proba_droite = nbr_donnees_droit/nbr_donnees_total

        nbr_0_gauche = self.répartition_classes(partitions["NoeudGauche"], "0")
        nbr_0_droite = self.répartition_classes(partitions["NoeudDroit"],"0")

        proba_0_si_gauche = nbr_0_gauche/nbr_donnees_gauche
        proba_0_si_droite = nbr_0_droite/nbr_donnees_droit
        proba_1_si_gauche = 1-proba_0_si_gauche
        proba_1_si_droite = 1-proba_0_si_droite

        entropie_gauche = -proba_0_si_gauche*self.log_(proba_0_si_gauche) - proba_1_si_gauche*self.log_(proba_1_si_gauche)
        entropie_droite = -proba_1_si_droite*self.log_(proba_1_si_droite) - proba_0_si_droite*self.log_(proba_0_si_droite)

        entropie = proba_gauche*entropie_gauche + proba_droite*entropie_droite           

        return entropie

    def log_(self, proba):
        """si proba est différent de zéro, retourne le logarithme en base 2 de proba et retourne 0 sinon"""
        if proba != 0:
            return log(proba, 2.0)
        else: 
            return 0

    def répartition_classes(self, donnees, classe):
        """Retourne le nombre de donnees pour lequel la classe est celle passée en paramètre"""
        nbr_apparitions = 0

        for donnee in donnees:
            if donnee[0] == "0":
                nbr_apparitions += 1

        return nbr_apparitions

    def valeurs_triées(self, donnees, attribut):
        """Pour un attribut donné, retourne une liste de toutes les valeurs que cet attribut prend dans le set de
        données, triées dans un ordre croissant et sans doublons"""

        if len(donnees) == 0 or attribut not in donnees[0][1]:
            return "Erreur: les donnees spécifiées sont vides ou incompatibles avec l'attribut spécifié" 

        valeurs = []

        for donnee in donnees:
            valeur = float(donnee[1][attribut])
            if valeur not in valeurs:
                valeurs.append(valeur)

        valeurs.sort()
        return valeurs



            


        



        
    
    