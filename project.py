from id3.moteur_id3.id3 import ID3
from id3.moteur_id3.id3_continu import ID3_continu

import pandas

from anytree import Node, RenderTree
from anytree.exporter import UniqueDotExporter
from anytree.render import ContRoundStyle
from anytree.dotexport import RenderTreeGraph

class ResultValues():

    def __init__(self):
        
        # Do computations here

        donnees = self.extract_data("data/train_bin.csv")
        donnees_continues = self.extract_data("data/train_continuous.csv")

        algo_id3 = ID3()
        algo_id3_continu = ID3_continu()
        
        # Task 1
        self.arbre = algo_id3.construit_arbre(donnees)
        # Task 3
        self.faits_initiaux = None
        self.regles = None
        # Task 5
        self.arbre_advance = algo_id3_continu.construit_arbre(donnees_continues)

    def get_results(self):
        return [self.arbre, self.faits_initiaux, self.regles, self.arbre_advance]
    
#METHODES QUE L'ON A AJOUTEES : 

    def extract_data(self, data_file):

        """Cette méthode permet l'importation d'un fichier de données dont le nom et chemin est passé en paramètre
           et la mise en forme de ces exemples dans la structure de données "données" utilisée dans le reste du projet
           Utilisation de la librairie pandas     
        """

        donnees_lues = pandas.read_csv(data_file)

        #Récupération des noms des attributs
        attributs_noms = donnees_lues.columns.values.tolist()
        attributs_noms.remove('target')

        classes = []
        donnees = []

        for i in range(len(donnees_lues)):
            
            #Récupération des valeurs des attributs
            attributs_valeurs = list(donnees_lues.values[i])
            attributs_valeurs = [str(i) for i in attributs_valeurs]
            #Récupération de la classification de chaque exemple
            classes.append(str(attributs_valeurs.pop(-1)))
            dico_attribut = dict(zip(attributs_noms, attributs_valeurs))

            donnees.append([classes[i], dico_attribut])
        
        return donnees

    def tree_analysis(self, arbre = None):

        """
        Fait appel à la méthode tree_analysis de la classe noeud de décision afin de ne parcourir l'arbre
        qu'une seule fois pour réaliser toutes les analyses (profondeur, profondeur moyenne, nombre d'enfants moyen)
        Par défaut l'arbre analysé est l'arbre commençant au niveau du noeud racine, mais il reste possible de fournir 
        un autre noeud de départ en paramètre
        """

        if arbre == None:
            return self.arbre.tree_analysis()     
        else:
            return arbre.tree_analysis()
    
    def model_eval(self, nom_fichier, continu = False):

        """
        Cette méthode permet d'évaluer le pourcentage de classifications correctes d'un arbre déjà construit
        à l'aide d'un second set de données dont le nom est passé en paramètre, par défaut analyse ID3 classique
        mais si le paramètre continu vaut False, analyse arbre_advance à la place
        """
        donnees = self.extract_data(nom_fichier)
        if len(donnees) == 0:
            print("Erreur, le fichier de test est vide")

        classifications_correctes = 0

        for donnee in donnees:
            if continu:
                classe_model = self.arbre_advance.classifie(donnee[1])
                classe_model = str(float(classe_model[-1]))
            else:
                classe_model = self.arbre.classifie(donnee[1])
                classe_model = str(float(classe_model[-1]))
                                
            if classe_model == donnee[0]:
                classifications_correctes+=1

        print("Le modèle classifie correctement " + str(100*(classifications_correctes/len(donnees))) + " pourcents des exemples.")

    def attributs_initialize(self):
        """Parcourt l'arbre dont self.arbre est la racine et initialise les attributs parent, nom, texte et risques
           (seulement pour les noeuds terminaux) de chaque noeud, cette étape est utile pour la méthode visual_tree
        """
        if self.arbre.enfants == None:
            return "Erreur"

        noeuds_à_explorer = [self.arbre]
        self.arbre.nom = "Racine"
        self.arbre.texte = "Racine"

        #permet de s'assurer de l'unicité de chaque nom
        i = 0

        while noeuds_à_explorer:
            noeud_courant = noeuds_à_explorer.pop(-1)

            if not(noeud_courant.terminal()):
                for valeur, enfant in noeud_courant.enfants.items():
                    noeuds_à_explorer.append(enfant)
                    enfant.parent = noeud_courant   
                    enfant.nom = noeud_courant.attribut + "_" + valeur + "___" + str(i)  
                    enfant.texte = noeud_courant.attribut + " = " + valeur
                    i+=1
            elif noeud_courant.terminal(): 
                if noeud_courant.classe() == "0":
                    noeud_courant.risques = "Risques faibles"

                elif noeud_courant.classe() == "1":
                    noeud_courant.risques = "Risques élevés"
                i+=1
    
    def visual_tree(self, noeud_racine = None): 

        """
        Traduit l'arbre calculé par ID3 sous une forme compréhensible pour la librairie anytree
        puis génère une version visuelle de l'arbre grâce à la librairie graphviz

        On rassemble les informations nécessaires pour créer les noeuds pour anytree 
        dans des listes de tuples

        Par défaut le noeud passé en argument est le noeud racine, si ce n'est pas le cas, il suffit de le passer en paramètre

        ATTENTION: la génération des fichiers png nécessite l'utilisation des deux commandes ci-dessous dans l'invite de commande:
        dot output/arbre.dot -T png -o output/arbre.png
        dot output/graphe.dot -T png -o output/graphe.png
        """

        #Permet d'initialiser l'attribut "parent" et "nom" de chaque noeud sauf la racine
        self.attributs_initialize()

        #Noeuds à explorer
        a_explorer = []

        #inclut les noeuds à explorer en commençant par la racine ou par le noeud de départ spécifié
        if noeud_racine == None or noeud_racine.nom == "Racine":
            #Dans le cas du noeud racine comme point de départ, on le traite à part et on commence au niveau des enfants (parce que le noeud racine n'a pas de noeud parent)
            for enfant in self.arbre.enfants.values():
                if not enfant.terminal():
                    a_explorer.append(enfant)
        else:
            a_explorer = [noeud_racine]

        #Génération du graphique possible seulement si le noeud de départ spécifié possède des enfants
        if a_explorer[0].enfants == None:
            return "Erreur"
                
        #Contient des tuples (nom_noeud, texte_à_afficher, nom_parent), chaque élément sous forme de string
        noeuds = []
        #Contient des tuples (nom_noeud, texte_spécifiant_classe, nom_parent), chaque élément sous forme de string
        noeuds_terminaux = []

        #Besoin de générer des noms uniques pour les feuilles
        i = 0

        #PARCOURS DE l'ARBRE ET GENERATION DES NOEUDS POUR ANYTREE
        
        while a_explorer:
            #On traite les noeuds pas encore explorés selon un algorithme DFS
            noeud_courant = a_explorer.pop(0)
            noeuds.append((noeud_courant.nom, noeud_courant.texte, noeud_courant.parent.nom))     
            
            for enfant in noeud_courant.enfants.values():
            
                if not(enfant.terminal()):
                    a_explorer.append(enfant)

                elif enfant.terminal():
                    noeuds.append((enfant.nom, enfant.texte, enfant.parent.nom))
                    nom_feuille = "noeud" + str(i)
                    noeuds_terminaux.append((nom_feuille, enfant.risques, enfant.nom))
                    i+=1
            
        # GENERATION DES NOEUDS POUR ANYTREE
        Racine = Node("Racine")
        nbr_noeuds_générés = 1

        for tup in noeuds:
            exec(tup[0] + " = Node(" + '"' + tup[1] + '"' + ", parent = " + tup[2] +")")
            nbr_noeuds_générés += 1
        for tup in noeuds_terminaux:
            exec(tup[0] + " = Node(" + '"' + str(tup[1]) + '"'+ ", parent = " + tup[2] +")")
            nbr_noeuds_générés += 1
        
        print("Nombre de noeuds générés = " + str(nbr_noeuds_générés))

        #GENERATION DU GRAPHIQUE PAR GRAPHVIZ ET ANYTREE
        print(RenderTree(Racine, style=ContRoundStyle()))

        RenderTreeGraph(Racine).to_dotfile("output/graphe.dot")
        UniqueDotExporter(Racine).to_dotfile("output/arbre.dot")
        
        
        


       
