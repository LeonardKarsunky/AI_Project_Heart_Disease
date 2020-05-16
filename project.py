#Utile pour toutes les parties
from id3.moteur_id3.id3 import ID3
from id3.moteur_id3.id3_continu import ID3_continu
import pandas
#Utile pour le bonus seulement
from anytree import Node, RenderTree
from anytree.exporter import UniqueDotExporter
from anytree.render import ContRoundStyle
from anytree.dotexport import RenderTreeGraph

class ResultValues():

    def __init__(self):
        
        # Importations des données pour les deux versions d'ID3
        donnees = self.extract_data("data/train_bin.csv")
        donnees_continues = self.extract_data("data/train_continuous.csv")

        # Création d'un instance pour les deux versions d'ID3
        algo_id3 = ID3()
        algo_id3_continu = ID3_continu()
        
        # Task 1
        self.arbre = algo_id3.construit_arbre(donnees)
        # Task 3
        """ ATTENTION
        self.faits_intiaux est initialisé par la fonction faits_initialize() qui demande 
        un nom de fichier en paramètre ainsi que l'index de l'exemple que l'on aimerait classifier
        OU une donnée directement
        """
        self.faits_initiaux = None    
        self.regles = self.regles_recherche()
        # Task 5
        self.arbre_advance = algo_id3_continu.construit_arbre(donnees_continues)

    def get_results(self):
        return [self.arbre, self.faits_initiaux, self.regles, self.arbre_advance]
    
#METHODES AJOUTEES : 

    def extract_data(self, data_file):

        """
        Cette méthode permet d'importer un fichier de données et de transformer et retourner son contenu 
        pour le rendre compatible avec l'algorithme d'ID3, c'est à dire sous la forme d'une structure 
        de données de forme suivante (chaque élément est stocké sous la forme de strings): 
        donnée := [classe, {attribut1:valeur1, ...}]

        Utilisation de la librairie pandas      
        """

        #Les données importées par la librairie pandas sont rassemblées dans une structure de données propre à la librairie appelée DataFrame
        donnees_lues = pandas.read_csv(data_file)

        #Récupération des noms des attributs
        attributs_noms = donnees_lues.columns.values.tolist()
        #En ignorant la dernière colonne qui correspond à la classe
        attributs_noms.remove('target')

        classes = []
        donnees = []

        #On parcourt les données 
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
        Fait appel à la méthode tree_analysis de la classe noeud de décision afin de réaliser une analyse complète de
        l'arbre passé stocké dans self.arbre (par défaut) ou d'un autre arbre que l'on passe en paramètre (noeud racine)
        On ne parcourt l'arbre qu'une seule fois pour réaliser toutes les analyses (profondeur max, profondeur moyenne, 
        nombre d'enfants moyen, nombre de noeuds terminaux et nombre de noeuds total)
        Retourne un string contenant le résultat de l'analyse
        """

        if arbre == None:
            return self.arbre.tree_analysis()     
        else:
            return arbre.tree_analysis()
    
    def model_eval(self, nom_fichier, advance = False):

        """
        Cette méthode permet d'évaluer le pourcentage de classifications correctes d'un arbre déjà construit
        à l'aide d'un set de données de test dont le nom du fichier est passé en paramètre. Par défaut, la méthode 
        analyse les performances de l'algorithme ID3 classique mais si le paramètre appelé advance vaut True,
        la méthode analyse arbre_advance à la place.
        Retourne un string contenant le résultat de l'analyse des performances.
        """

        #Extraction des données du set de test
        donnees = self.extract_data(nom_fichier)

        #Erreur si le fichier est vide ou incompatble avec notre méthode extract_data
        if len(donnees) == 0:
            print("Erreur, le fichier de test est vide")

        #Compteur des classifications correctes
        classifications_correctes = 0

        #On parcourt les données du set de test
        for donnee in donnees:
            #On traite soit self.arbre soit self.arbre_advance selon la valeur du paramètre "advance"
            if advance:
                classe_model = self.arbre_advance.classifie(donnee[1])
                classe_model = str(float(classe_model[-1]))
            else:
                classe_model = self.arbre.classifie(donnee[1])
                classe_model = str(float(classe_model[-1]))

            #On incrémente sur le compteur lorsqu'une classification est correcte          
            if classe_model == str(float(donnee[0])):
                classifications_correctes+=1

        rep = ("Le modèle classifie correctement " + str(100*(classifications_correctes/len(donnees))) + " pourcents des exemples.")
        return rep

    def regles_recherche(self):
        """
        Cette méthode permet de générer une liste de règles sous la forme d'une liste de listes de strings
        à partir d'un arbre de décision déjà créé et stocké dans self.arbre. Retourne la liste de règles
        """

        self.attributs_initialize()

        #liste des noeuds pas encore explorés
        noeuds_à_explorer = [self.arbre]

        #Règle modifiée dynamiquement pendant le parcours de l'arbre (liste de strings)
        règle = []

        #Règles finales (liste de listes de strings)
        règles_finales = []

        #Tant qu'on a pas exploré tout l'arbre
        while noeuds_à_explorer:

            #On explore selon le DFS (last in first out)
            noeud_courant = noeuds_à_explorer.pop(-1)

            #On à atteint un noeud terminal au tour de boucle précédant et on a remonté dans l'arbre. La règle est mise à jour.
            if len(règle) > noeud_courant.depth:
                nbr_de_strings_à_enlever = len(règle) - (noeud_courant.depth) 

                #On ôte de règle les strings dont on a plus besoins (la fin de la règle) mais on conserve ceux qui sont encore utiles (le début de la règle)
                for _ in range(nbr_de_strings_à_enlever):
                    del règle[-1]

            #On ajoute le string du noeud courant à la règle
            règle.append(noeud_courant.texte)

            #Si le noeud est terminal, on ajoute la règle à la liste de règles finales, en ajoutant la conclusion de la règle
            if noeud_courant.terminal():
                règle_à_ajouter = règle[1:]
                règle_à_ajouter.append(noeud_courant.classe()) 
                règles_finales.append(règle_à_ajouter)
            
            else:
                #Si le noeud n'est pas terminal, on traite les enfants
                for enfant in noeud_courant.enfants.values():
                    noeuds_à_explorer.append(enfant)
                    enfant.depth = noeud_courant.depth + 1

        return règles_finales

    def classification_regles(self):
        """
        Permet de classifier l'exemple dont la donnée est stockée dans l'attribut self.faits_initiaux à l'aide
        des règles générées à partir de l'arbre et stockées dans l'attributs self.regles
        ATTENTION : nécessite l'appel préalable de la méthode faits_initialize
        """
        if self.faits_initiaux == None:
            rep = "S'il vous plaît, veuillez initialiser l'attribut faits_initiaux grâce à la méthode faits_initialize"
            return rep

        donnee = []

        #La donnée est transformée sous la forme d'une liste de strings afin de faciliter la comparaison avec les conditions de la règle
        for attribut, valeur in self.faits_initiaux.items():
            donnee.append(str(attribut + " = " + valeur))

        #on compare pour chaque règle le nombre de faits partagés entre la règle et la donnée...
        for regle in self.regles:
            faits_partagés = 0

            for fait in regle:
                if fait in donnee:
                    faits_partagés += 1

            #Si le nombre de faits partagés est égal au nombre de conditions de la règle (sauf la conclusion, d'où le -1), la règle permet de classifier l'exemple
            if faits_partagés == len(regle) - 1 :
                rep = "La donnée : " + '\n' + str(donnee) + '\n' + " est dans la classe : " + regle[-1] + '\n'
                regle = regle[:-1]
                for fait in regle:
                    rep += " Parce que " + fait + '\n'
                return rep
            
        #Si aucune règle ne permet de classifier exactement l'exemple, on utilise la méthode classifie de NoeudDeDecision
        rep = "Pas de classification trouvée grâce aux règles"
        return rep
            
    def faits_initialize(self, nom_fichier = None, indice_exemple = None, donnee = None):
        """
        Permet d'initialiser self.faits_initiaux avec une donnée directement (dictionnaire attribut:valeur) ou
        en spécifiant un fichier externe contenant des données et l'indice de l'exemple d'intérêt 
        """

        if donnee == None and nom_fichier != None and indice_exemple != None:
            donnees = self.extract_data(nom_fichier)
            self.faits_initiaux = donnees[indice_exemple][1]
        elif nom_fichier == None and indice_exemple == None and donnee != None:
            self.faits_initiaux =  donnee
        else:
            print("Erreur: vous avez incorrectement utilisé la méthode")         
        
    def attributs_initialize(self):
        """Parcourt l'arbre dont self.arbre est la racine et initialise les attributs parent, nom et texte 
           de chaque noeud et l'attribut risques en plus pour les noeuds terminaux, cette étape est utile pour la méthode visual_tree
           et pour la méthode regle_recherche qui bénéficie de l'attribut texte
        """
        if self.arbre.enfants == None:
            return "Erreur"

        noeuds_à_explorer = [self.arbre]
        self.arbre.nom = "Racine"
        self.arbre.texte = "Racine"

        #permet de s'assurer de l'unicité de chaque nom stocké dans l'attribut nom de chaque Noeud (important car chaque nom sera utilisé plus tard comme nom de variable)
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
        
        
        


       
