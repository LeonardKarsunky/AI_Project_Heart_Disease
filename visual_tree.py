import os

os.environ["PATH"] += os.pathsep + 'C:\Program Files (x86)\Graphviz2.38/bin/'

from anytree import Node, RenderTree
from anytree.exporter import DotExporter
from anytree.render import ContRoundStyle
from anytree.dotexport import RenderTreeGraph
from graphviz import render

from id3.moteur_id3.noeud_de_decision import NoeudDeDecision
from id3.moteur_id3.id3 import ID3
from project import ResultValues

instance = ResultValues("data/train_bin.csv")
#résultats = instance.get_results()
#print(résultats)

instance.visual_tree()

def visual_tree(self, noeud_racine = True): 

        """
        Traduit l'arbre calculé par ID3 sous une forme compréhensible pour la librairie anytree
        puis génère une version visuelle de l'arbre grâce à la librairie graphviz

        On rassemble les informations nécessaires pour créer les noeuds pour anytree 
        dans des listes de tuples

        Par défaut le noeud passé en argument est le noeud racine, si ce n'est pas le cas l'indiquer en passant False en paramètre
        """

        #Génération du graphique possible seulement si le noeud racine possède des enfants
        if self.arbre.enfants == None:
            return "Erreur"

        #inclut les noeuds à explorer en commençant par la racine
        a_explorer = [self.arbre]
        
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
            if noeud_racine == True:
                nom_papa  = "racine"
                noeud_racine = False
                    
            else:
                nom_papa = papa.nom          
            
            for valeur, enfant in papa.enfants.items():
                
                nom_enfant = papa.attribut + "_" + str(valeur)
                texte_enfant = papa.attribut + " = " + str(valeur)
                noeuds.append((nom_enfant, texte_enfant, nom_papa))
                enfant.nom = nom_enfant

                if not(enfant.terminal()):
                    a_explorer.append(enfant)
                else:
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

        RenderTreeGraph(racine).to_dotfile("output/arbre.dot")
        render('dot', 'png', 'output/arbre.dot')
       

        """
        (graph,) = pydot.graph_from_dot_file("output/arbre.dot")
        graph.write_png("output/arbre.png")
        output_file.close()
        """