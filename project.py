from id3.moteur_id3.noeud_de_decision import NoeudDeDecision
from id3.moteur_id3.id3 import ID3
import pandas

from anytree import Node, RenderTree
from anytree.exporter import UniqueDotExporter
from anytree.render import ContRoundStyle
from anytree.dotexport import RenderTreeGraph

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
    
#Méthodes rajoutées par nous : 

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
    
    def model_eval(self, nom_fichier):

        """
        Cette méthode permet d'évaluer le pourcentage de classifications correctes d'un arbre déjà construit
        à l'aide d'un second set de données dont le nom est passé en paramètre
        """

        donnees = self.extract_data(nom_fichier)
        if len(donnees) == 0:
            return 0
        classification = 0

        for donnee in donnees:
            classe_model = self.arbre.classifie(donnee[1])
            classe_model = classe_model[-1]
            if classe_model == donnee[0]:
                classification+=1

        print("Le modèle classifie correctement " + str(100*(classification/len(donnees))) + " pourcents des exemples.")

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

        #Génération du graphique possible seulement si le noeud racine possède des enfants
        if self.arbre.enfants == None:
            return "Erreur"

        #inclut les noeuds à explorer en commençant par la racine
        if noeud_racine == None:
            a_explorer = [self.arbre]
        else:
            a_explorer = [noeud_racine]
        
        #Contient des tuples (nom_noeud, texte_à_afficher, nom_parent), chaque élément sous forme de string
        noeuds = []
        #Contient des tuples (nom_noeud, texte_spécifiant_classe, nom_parent), chaque élément sous forme de string
        noeuds_terminaux = []

        i = 0
        #PARCOURS DE l'ARBRE ET GENERATION DES NOEUDS POUR ANYTREE
        
        while a_explorer:
            #On traite les noeuds pas encore explorés (DFS)
            papa = a_explorer.pop(0)

            #Traitement spécial au premier tour de la boucle à cause de la racine
            if noeud_racine == None:
                nom_papa  = "racine"
                noeud_racine = 1
                    
            else:
                nom_papa = papa.nom          
            
            for valeur, enfant in papa.enfants.items():
                
                nom_enfant = papa.attribut + "_" + str(valeur)
                texte_enfant = papa.attribut + " = " + str(valeur)
                noeuds.append((nom_enfant, texte_enfant, nom_papa))
                enfant.nom = nom_enfant

                if not(enfant.terminal()):
                    a_explorer.append(enfant)
                elif enfant.terminal():
                    #Traitement des noeuds terminaux
                    nom_noeud = "noeud"+ str(i)
                    risques = ""

                    if enfant.classe() == "0":
                        risques += "Risques faibles"
                    elif enfant.classe() == "1":
                        risques += "Risques élevés"
                    noeuds_terminaux.append((nom_noeud, risques, nom_enfant))

                    i+=1 

        # GENERATION DES NOEUDS POUR ANYTREE
        racine = Node("Racine")

        for tup in noeuds:
            exec(tup[0] + " = Node(" + '"' + tup[1] + '"' + ", parent = " + tup[2] +")")
        for tup in noeuds_terminaux:
            exec(tup[0] + " = Node(" + '"' + tup[1] + '"'+ ", parent = " + tup[2] +")")

        #GENERATION DU GRAPHIQUE PAR GRAPHVIZ ET ANYTREE
        print(RenderTree(racine, style=ContRoundStyle()))

        RenderTreeGraph(racine).to_dotfile("output/graphe.dot")
        UniqueDotExporter(racine).to_dotfile("output/arbre.dot")
        
        
        


       
