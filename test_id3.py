from id3.moteur_id3.noeud_de_decision import NoeudDeDecision
from id3.moteur_id3.id3 import ID3
from project import ResultValues


instance = ResultValues("data/train_bin.csv")
résultats = instance.get_results()

print(résultats)

donnees = instance.extract_data("data/train_bin.csv")






"""
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import plot_tree

#import matplotlib.pyplot as plt
#import sklearn

X = []
Y = []

for donnee in donnees:
    Y.append(donnee[0])
    X.append


classifier = DecisionTreeClassifier("entropy")
classifier = classifier.fit()
"""
    