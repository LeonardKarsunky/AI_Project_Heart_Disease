from id3.moteur_id3.noeud_de_decision import NoeudDeDecision
from id3.moteur_id3.id3 import ID3
from id3.moteur_id3.id3_continu import ID3_continu
from project import ResultValues
import random
import statistics

instance = ResultValues()
#résultats = instance.get_results()

"PARTIE 1: permet d'obtenir quelques statistiques concernant l'arbre généré"

#print(instance.arbre)
#print(instance.tree_analysis())

"PARTIE 2 : permet d'obtenir une évaluation des performances de l'arbre"

#print(instance.model_eval("data/test_public_bin.csv"))

"PARTIE 3 : permet de générer un ensemble de règles à partir de l'arbre et de les utiliser pour classifier un exemple"

#print(instance.regles)

"""Exemple d'utilisation à partir d'un fichier de données et d'un indice d'exemple"""
#indice = 35 #ATTENTION l'indice indiqué par la colonne de gauche dans le fichier excel est décalé de 2 par rapport à l'indice ci-contre (ne commence pas à zéro et la ligne 1 est occupée par le nom des attributs)
#instance.faits_initialize("data/test_public_bin.csv", indice)
#print(instance.classification_regles())

"""Exemple d'utilisation à partir d'une donnée"""
#attributs = ["age","sex","cp","trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"]
#valeurs = ["2","1","3","1","2","0","1","2","0","1","1","0","3"]
#dico = dict(zip(attributs, valeurs))
#instance.faits_initialize(None, None, dico)
#print(instance.classification_regles())

"PARTIE 4 :"


"PARTIE 5 :"
#print(instance.arbre_advance)
#print(instance.arbre_advance.tree_analysis())

#print(instance.model_eval("data/test_public_continuous.csv", True))



"""
BONUS_1:
Décommenter la ligne ci-dessous pour générer les représentations graphiques (sauvées dans le dossier output) et 
compléter par le lancement des deux commandes suivantes dans le terminal depuis le dossier Projet:
dot output/arbre.dot -T png -o output/arbre.png 
dot output/graphe.dot -T png -o output/graphe.png
"""
#instance.visual_tree()

"""BONUS_2
La fonction définie ci-dessous permet d'effectuer une cross validation en utilisant en plus des données d'entraînements
(nom du fichier passé en argument) un certain pourcentage (paramètre) des données de test (nom du fichier passé en argument)
afin de générer un meilleur modèle. Cette opération est répétée un certain nombre de fois (paramètre) avec la part des données de test choisie pour faire partie des données
d'entraînement chaque fois différente (selectionnée aléatoirement). La fonction retourne une moyenne du pourcentage 
de classifications correctes. La méthode peut être utilisée sur ID3 ou ID3_continu.

Appel de la fonction situé en dessous de la définition fonction
"""

def cross_validation(donnees_entrainement, donnees_test, pourcentage, repetitions, advance):

    if advance:
        algo_id3 = ID3_continu()
    else:
        algo_id3 = ID3()

    #Importations des données d'entraînement et de test
    donnees_entr = instance.extract_data(donnees_entrainement)
    donnees_test = instance.extract_data(donnees_test)
    #Nombre de données provenant des données de test ajoutées aux données d'entraînements
    nbr_donnees_additionnelles = int(len(donnees_test)*pourcentage)

    pourcentages = []

    for _ in range(repetitions):
        
        #Les données à ajouter aux données d'entraînement
        donnees_sup = random.sample(donnees_test, k = nbr_donnees_additionnelles)
        donnees = donnees_entr + donnees_sup
        #Les données restantes servant de données de test
        donnees_restantes = []
        for donnee in donnees_test:
            if donnee not in donnees_sup:
                donnees_restantes.append(donnee)

        arbre = algo_id3.construit_arbre(donnees)

        instance.tree_setter(arbre, advance)
        pourcentages.append(instance.model_eval(None, advance, donnees_restantes, False))
    
    rep = "Pour une cross-validation utilisant " + str(pourcentage*100) + " pourcents des exemples des données de test afin de créer " 
    rep += str(repetitions) + " arbres différents, le pourcentage moyen de classifications correctes est : "
    rep += str(statistics.mean(pourcentages)) + " pourcents."
    return rep

#print(cross_validation("data/train_bin.csv", "data/test_public_bin.csv", 0.8, 150, False))
#print(cross_validation("data/train_continuous.csv", "data/test_public_continuous.csv", 0.8, 30, True))
