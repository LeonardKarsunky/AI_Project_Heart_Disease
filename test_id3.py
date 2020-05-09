from id3.moteur_id3.noeud_de_decision import NoeudDeDecision
from id3.moteur_id3.id3 import ID3
from project import ResultValues


instance = ResultValues("data/train_bin.csv")
résultats = instance.get_results()
#print(résultats)

"PARTIE 1: permet d'obtenir quelques statistiques concernant l'arbre"
#print(instance.tree_analysis())

"PARTIE 2 : permet d'obtenir une évaluation des capacités de l'arbre"
instance.model_eval("data/test_public_bin.csv")


"""
BONUS:
Décommenter la ligne suivante pour générer les représentations graphiques (sauvées dans le dossier output) et 
compléter par le lancement des deux commandes suivantes dans le terminal depuis le dossier Projet:
dot output/arbre.dot -T png -o output/arbre.png 
dot output/graphe.dot -T png -o output/graphe.png
"""

#instance.visual_tree()
