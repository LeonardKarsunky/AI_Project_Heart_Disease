import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.datasets import load_breast_cancer
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from sklearn import tree

from id3.moteur_id3.noeud_de_decision import NoeudDeDecision
from id3.moteur_id3.id3 import ID3
from project import ResultValues


instance = ResultValues("data/train_bin.csv")
donnees = instance.extract_data("data/train_bin.csv")

#train_test_split(*arrays, **options)

print(résultats)




