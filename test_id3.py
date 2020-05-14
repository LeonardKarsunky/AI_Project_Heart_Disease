from id3.moteur_id3.noeud_de_decision import NoeudDeDecision
from id3.moteur_id3.id3 import ID3
from id3.moteur_id3.id3_continu import ID3_continu
from project import ResultValues


instance = ResultValues()
#résultats = instance.get_results()

"PARTIE 1: permet d'obtenir quelques statistiques concernant l'arbre généré"
#print(instance.arbre)
#print(instance.tree_analysis())

"PARTIE 2 : permet d'obtenir une évaluation des capacités de l'arbre"
#instance.model_eval("data/test_public_bin.csv")

"PARTIE 3 :"

"PARTIE 4 :"


"PARTIE 5 :"
print(instance.arbre_advance)
print(instance.arbre_advance.tree_analysis())

print(instance.model_eval("data/test_public_continuous.csv", True))












"""
BONUS:
Décommenter la ligne suivante pour générer les représentations graphiques (sauvées dans le dossier output) et 
compléter par le lancement des deux commandes suivantes dans le terminal depuis le dossier Projet:
dot output/arbre.dot -T png -o output/arbre.png 
dot output/graphe.dot -T png -o output/graphe.png
"""
#instance.visual_tree()
