from id3.moteur_id3.noeud_de_decision import NoeudDeDecision
from id3.moteur_id3.id3 import ID3
import pandas

class ResultValues():

    def __init__(self, nom_fichier):
        
        # Do computations here

        donnees = self.extract_data(nom_fichier)
        algo_id3 = ID3()
        
        # Task 1
        self.arbre = algo_id3.construit_arbre(donnees)
        # Task 3
        self.faits_initiaux = None
        self.regles = None
        # Task 5
        self.arbre_advance = None

    def get_results(self):
        return [self.arbre, self.faits_initiaux, self.regles, self.arbre_advance]
    
    def extract_data(self, data_file):

        donnees_lues = pandas.read_csv(data_file)

        attributs_noms = donnees_lues.columns.values.tolist()
        attributs_noms.remove('target')

        classes = []
        donnees = []

        for i in range(donnees_lues.index.stop):
        
            attributs_valeurs = list(donnees_lues.values[i])
            classes.append(attributs_valeurs.pop(-1))
            dico_attribut = dict(zip(attributs_noms, attributs_valeurs))

            donnees.append([classes[i], dico_attribut])

        return donnees



