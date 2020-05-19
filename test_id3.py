from id3.moteur_id3.noeud_de_decision import NoeudDeDecision
from id3.moteur_id3.id3 import ID3
from id3.moteur_id3.id3_continu import ID3_continu
from project import ResultValues

#Utile pour cross-validation
import statistics
from random import shuffle


instance = ResultValues()
#résultats = instance.get_results()

"PARTIE 1: permet d'obtenir quelques statistiques concernant l'arbre généré"

#print(instance.tree_analysis())

"PARTIE 2 : permet d'obtenir une évaluation des performances de l'arbre"

#print(instance.model_eval("data/test_public_bin.csv"))

"PARTIE 3 : permet de générer un ensemble de règles à partir de l'arbre et de les utiliser pour classifier un exemple"

#print(instance.regles)

"Exemple d'utilisation à partir d'un fichier de données et d'un indice d'exemple"

#indice = 0 #ATTENTION l'indice indiqué par la colonne de gauche dans le fichier excel est décalé de 2 par rapport à l'indice ci-contre (dans le fichier excel, on ne commence pas à l'indice zéro et la ligne 1 est occupée par le nom des attributs)
#instance.faits_initialize("data/test_public_bin.csv", indice) #Premier exemple du fichier test_public_bin

#print(instance.classification_regles())

"Exemple d'utilisation à partir d'une donnée "

#attributs = ["age","sex","cp","trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"]
#valeurs = ["2","1","3","1","2","0","1","2","0","1","1","0","3"]
#dico = dict(zip(attributs, valeurs))   #Premier exemple du fichier test_public_bin
#instance.faits_initialize(None, None, dico)

#print(instance.classification_regles())

"PARTIE 4 : Génération d'un diagnostic à partir d'une donnée "

#attributs = ["age","sex","cp","trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"]
#valeurs = ["3","1","1","2","1","1","0","3","0","1","2","0","2"]
#dico = dict(zip(attributs, valeurs)) #Exemple numéro 2 du fichier test_public_bin, classifié comme "à risques"

#print(instance.diagnostic(dico))


"PARTIE 5 : Génération"
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
La fonction définie ci-dessous permet d'effectuer une cross validation. On merge les données de test et les données
d'entraînement, on sépare cet ensemble de données en k sous-ensembles. On entraîne ID3 sur k-1 des sous-ensembles
et on évalue les performances de l'arbre sur le sous-ensemble restant. On répète l'opération jusqu'à ce que chacun
des k sous-ensembles ait servi d'ensemble test. Le résultat de cette fonction est la moyenne des performances de
chaque arbre. La méthode peut être utilisée sur ID3 ou ID3_continu (mais de par le manque d'optimisation
le temps de calcul de la cross-validation pour ID3_continu est assez conséquent)

Appel de la fonction situé en dessous de la définition de la fonction
"""

def cross_validation(donnees_entrainement, donnees_test, k, advance):

    if advance:
        algo_id3 = ID3_continu()
    else:
        algo_id3 = ID3()

    #Importations des données d'entraînement et de test
    donnees_entr = instance.extract_data(donnees_entrainement)
    donnees_test = instance.extract_data(donnees_test)

    #Merge de ces deux groupes de données
    donnees = donnees_entr + donnees_test
    shuffle(donnees)

    #Les sous-ensembles sont stockés dans une liste de liste de données
    ss_ensembles = []
    ss_ensemble_temp = []

    #Nombre de données par sous-ensemble
    nbr_donnees = int(len(donnees)/k)

    #Permet de stocker les performances de chaque arbre
    performances = []
    #On crée les ss-ensembles (chacun a exactement la même taille, au risque de laisser quelques données inutilisées)
    for donnee in donnees:
        ss_ensemble_temp.append(donnee)

        if len(ss_ensemble_temp) == nbr_donnees:
            ss_ensembles.append(ss_ensemble_temp)
            ss_ensemble_temp = []

    #on parcourt chaque ss-ensemble jusqu'à ce que chacun...
    for ss_ensemble in ss_ensembles:
        
        #... ait servi d'ensemble test
        ensemble_test = ss_ensemble
        #On initialise l'ensemble d'entraînement avec les données des autres ss-ensembles
        ensemble_entr = []
        for ss_ensemble in ss_ensembles:
            if ss_ensemble != ensemble_test:
                for donnee in ss_ensemble:
                    ensemble_entr.append(donnee)
        
        arbre = algo_id3.construit_arbre(ensemble_entr)

        instance.tree_setter(arbre, advance)

        performances.append(instance.model_eval(None, advance, ensemble_test, False))
    
    rep = "Pour une " + str(k) + "-fold cross-validation, les performances de l'arbre sont en moyenne de " 
    rep += str(round(statistics.mean(performances),3)) + " pourcents de classifications correctes."
    return rep

""" Cross-validation """
#k = 22
#print(cross_validation("data/train_bin.csv", "data/test_public_bin.csv", k, False))
#print(cross_validation("data/train_continuous.csv", "data/test_public_continuous.csv", k, True))
