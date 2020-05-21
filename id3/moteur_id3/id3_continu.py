from math import log
from .noeud_de_decision_continu import NoeudDeDecision_continu
from .id3 import ID3
import random, math

class ID3_continu(ID3):

    #Méthodes redéfinies par ID3_continu par rapport à la classe mère : 

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

        # Si toutes les données du noeud font parties de la même classe, on a affaire à un noeud terminal        
        elif self.classe_unique(donnees):
            return NoeudDeDecision_continu(None, donnees, str(predominant_class))
            
            # Sinon, on sélectionne l'attribut et la valeur qui minimise l'entropie
        else:
            attr_et_val = self.attribut_valeur_min_entropie(donnees, attributs)
            attribut = attr_et_val[0]
            valeur = attr_et_val[1]
            
            # On partitionne les données en fonction de cette valeur de partitionnement et de cet attribut)
            partitions = self.partitionne_binaire(donnees, attribut, valeur)        
            
            # GRâce à ce partitionnement on peut définir les deux noeuds enfants 
            enfants = {}

            #L'enfant gauche possède toutes les données dont l'attribut de partitionnement a une valeur inférieure à la valeur de partitionnement
            enfants["NoeudGauche"] = self.construit_arbre_recur(partitions["NoeudGauche"], attributs, predominant_class)
            #L'enfant droit possède toutes les données dont l'attribut de partitionnement a une valeur supérieure à la valeur de partitionnement             
            enfants["NoeudDroit"] = self.construit_arbre_recur(partitions["NoeudDroit"], attributs, predominant_class)
            
            #On construit l'arbre récursivement
            return NoeudDeDecision_continu(attribut, donnees, str(predominant_class), enfants, valeur)


    #Nouvelles méthodes spécifiques à ID3_continu :
            
    def partitionne_binaire(self, donnees, attribut, valeur_de_part):
        """ Partitionne les données en les séparant de façon binaire avec d'un côté les
        données pour lesquelles la valeur de l'attribut spécifié est inférieure à la valeur_de_part et de 
        l'autre les données dont la valeur de l'attribut est supérieure à la valeur_de_part

            :param list donnees: les données à partitioner.
            :param attribut: l'attribut de partitionnement.
            :param valeur_de_part: la valeur au niveau de laquelle on coupe le jeu de données en deux
            :return: un dictionnaire qui associent aux deux clés "NoeudGauche" et "NoeuDroit" les deux listes de données correspondantes
        """
        partitions = {}
        #L'enfant gauche possède toutes les données dont l'attribut de partitionnement a une valeur inférieure à la valeur de partitionnement
        partitions["NoeudGauche"] = []
        #L'enfant droit possède toutes les données dont l'attribut de partitionnement a une valeur supérieure à la valeur de partitionnement 
        partitions["NoeudDroit"] = []
        
        for donnee in donnees:
            #La donnée fait partie du noeud enfant gauche
            if float(donnee[1][attribut]) < valeur_de_part:
                partitions["NoeudGauche"].append(donnee)
            #La donnée fait partie du noeud enfant droit
            elif float(donnee[1][attribut]) >= valeur_de_part:
                partitions["NoeudDroit"].append(donnee)
        
        return partitions
    



    def attribut_valeur_min_entropie(self, donnees, attributs):
        """
        Cherche parmi tous les attributs et toutes leurs valeurs, l'attribut et la valeur minimisant le mieux l'entropie
        Et retourne cet attribut et sa valeur de partitionnement correspondante sous forme d'une liste [attribut, valeur]
        :param donnees : les données du noeud père
        :param attributs : liste de strings contenant les noms des attributs
        :return : liste de forme [attribut_optimal, valeur_optimale]
        """
        
        if len(donnees) == 0:
            return "Erreur les données spécifiées sont vides"

        #Dico de forme {attribut:[valeur_de_partitionnment_minimisant_l'entropie, entropie correspondante]}
        dico_attribut_entropie = {}

        #Remplit ce dictionnaire à l'aide de la méthode valeur_min_entropie
        for attribut in attributs:
            #Recherche pour chaque attribut LA valeur de partitionnement qui minimise l'entropie
            dico_attribut_entropie[attribut] = self.valeur_min_entropie(donnees, attribut)

        entropie_min = 999.9
        valeur_de_partitionnement = -1.0
        attribut_de_partitionnement = ""

        #Recherche parmi tous les attributs celui qui minimise le mieux l'entropie
        for attribut, val_et_entropie in dico_attribut_entropie.items():
            entropie_courante = val_et_entropie[1]
            if entropie_courante < entropie_min:
                entropie_min = entropie_courante
                valeur_de_partitionnement = val_et_entropie[0]
                attribut_de_partitionnement = attribut
        
        #On retourn l'attribut optimal et sa valeur de partitionnement correspondante
        return [attribut_de_partitionnement, valeur_de_partitionnement]




    def valeur_min_entropie(self, donnees, attribut):
        """ Cherche pour l'attribut spécifié, la valeur qui une fois choisie pour partitionner les données en
            deux sous-ensembles, minimiserait l'entropie et retourne une liste contenant [valeur_minimisant_entropie, entropie_correspondante]

            :param donnees : les données du noeud père
            :param attribut : l'attribut dont on aimerait trouver la valeur de partitionnement minimisant l'entropie
            :return : liste de forme [valeur_minimisant_entropie, entropie_correspondante]
        """

        if len(donnees) <= 1:
            return "Erreur les donnees spécifiées ne peuvent plus être partitionnées"

        #Trie toutes les valeurs apparaissant dans le set de données de l'attribut spécifié par ordre croissant
        valeurs_triées = self.valeurs_triées(donnees, attribut)
        #On enlève la première valeur car la choisir comme valeur de partitionnement résulterait à avoir un noeud enfant gauche vide
        del valeurs_triées[0]
  
        valeur_finale = -1.0
        entropie_min = 999.9

        #Recherche de la valeur minimisant l'entropie
        for valeur in valeurs_triées:
    
            entropie_temp = self.entropie_part_binaire(donnees, attribut, valeur)
            if entropie_temp < entropie_min:
                entropie_min = entropie_temp
                valeur_finale = valeur
        
        #On retourne une lsite de forme  [valeur_minimisant_entropie, entropie_correspondante]
        return [valeur_finale, entropie_min]                     




    def entropie_part_binaire(self, donnees, attribut, valeur_de_part):
        """Retourne pour un set de données, un attribut spécifique et une valeur de partionnement pour l'attribut, 
        l'entropie totale (somme de l'entropie des deux sous-ensembles résultants) """

        #On commence par partitionner de façon binaire les donnees en fonction de l'attribut et de la valeur_de_partionnement spécifiés
        partitions = self.partitionne_binaire(donnees, attribut, valeur_de_part)

        #Calcul de p_aj :
        nbr_donnees_gauche = len(partitions["NoeudGauche"])
        nbr_donnees_droit = len(partitions["NoeudDroit"])
        nbr_donnees_total = len(donnees)

        proba_gauche = nbr_donnees_gauche/nbr_donnees_total
        proba_droite = nbr_donnees_droit/nbr_donnees_total

        #Calcul de p_ci_aj : 
        nbr_0_gauche = self.répartition_classes(partitions["NoeudGauche"], "0")
        nbr_0_droite = self.répartition_classes(partitions["NoeudDroit"],"0")

        proba_0_si_gauche = nbr_0_gauche/nbr_donnees_gauche
        proba_0_si_droite = nbr_0_droite/nbr_donnees_droit
        proba_1_si_gauche = 1-proba_0_si_gauche
        proba_1_si_droite = 1-proba_0_si_droite

        #Calcul de H_C_aj
        entropie_gauche = -proba_0_si_gauche*self.log_(proba_0_si_gauche) - proba_1_si_gauche*self.log_(proba_1_si_gauche)
        entropie_droite = -proba_1_si_droite*self.log_(proba_1_si_droite) - proba_0_si_droite*self.log_(proba_0_si_droite)

        #Calcul de H_C_A
        entropie = proba_gauche*entropie_gauche + proba_droite*entropie_droite  

        return entropie




    def log_(self, proba):
        """si la probabilité est différente de zéro, retourne le logarithme en base 2 de proba et retourne 0 sinon"""
        if proba != 0.0:
            return log(proba, 2.0)
        else: 
            return 0.0




    def répartition_classes(self, donnees, classe):
        """
        Retourne le nombre de données classifiées par la classe spécifiée parmi les données spécifiées
        """

        nbr_apparitions = 0
        classe = str(float(classe))

        for donnee in donnees:
            if donnee[0] == classe:
                nbr_apparitions += 1

        return nbr_apparitions



    def valeurs_triées(self, donnees, attribut, doublons = False):
        """Pour un attribut donné, retourne une liste de toutes les valeurs que cet attribut prend dans le set de
        données, triées dans un ordre croissant et avec ou sans doublons"""

        if len(donnees) == 0 or attribut not in donnees[0][1]:
            return "Erreur: les donnees spécifiées sont vides ou incompatibles avec l'attribut spécifié" 

        valeurs = []

        for donnee in donnees:
            valeur = float(donnee[1][attribut])
            if not(doublons) and valeur not in valeurs:
                valeurs.append(valeur)
            elif doublons:
                valeurs.append(valeur)

        valeurs.sort()
        return valeurs

  



            


        



        
    
    