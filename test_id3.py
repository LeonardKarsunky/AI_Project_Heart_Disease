from id3.moteur_id3.noeud_de_decision import NoeudDeDecision
from id3.moteur_id3.id3 import ID3
from id3.moteur_id3.id3_continu import ID3_continu
from project import ResultValues


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
BONUS:
Décommenter la ligne ci-dessous pour générer les représentations graphiques (sauvées dans le dossier output) et 
compléter par le lancement des deux commandes suivantes dans le terminal depuis le dossier Projet:
dot output/arbre.dot -T png -o output/arbre.png 
dot output/graphe.dot -T png -o output/graphe.png
"""
#instance.visual_tree()
