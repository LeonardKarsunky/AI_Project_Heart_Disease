#Utile pour toutes les parties 1 à 5
from id3.moteur_id3.id3 import ID3
from id3.moteur_id3.id3_continu import ID3_continu
import pandas
#Utile pour le bonus 1 : visualisation de l'arbre
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
        OU une donnée directement. Peut également être modifié par la méthode diagnostic.
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
    


    def model_eval(self, advance, rep_print, nom_fichier = None, donnees = None):

        """
        Cette méthode permet d'évaluer le pourcentage de classifications correctes d'un arbre déjà construit
        à l'aide d'un set de données de test dont le nom du fichier est passé en paramètre. Par défaut, la méthode 
        analyse les performances de l'algorithme ID3 classique mais si le paramètre appelé advance vaut True,
        la méthode analyse arbre_advance à la place.
        Retourne un string contenant le résultat de l'analyse des performances.
        """
        if nom_fichier != None:
            #Extraction des données du set de test
            donnees = self.extract_data(nom_fichier)
        else:
            #utile pour la fonction de cross-validation dans test_id3.py
            donnees = donnees

        #Erreur si le fichier est vide ou incompatble avec notre méthode extract_data
        if len(donnees) == 0:
            print("Erreur, le fichier de test est vide")

        #Compteur des classifications correctes
        classifications_correctes = 0

        #On parcourt les données du set de test
        for donnee in donnees:
            #On traite soit self.arbre soit self.arbre_advance selon la valeur du paramètre "advance"
            if advance:
                classe_model = str(float(self.arbre_advance.classifie(donnee[1], False)))
            else:
                classe_model = str(float(self.arbre.classifie(donnee[1], False)))

            #On incrémente sur le compteur lorsqu'une classification est correcte          
            if classe_model == str(float(donnee[0])):
                classifications_correctes+=1
        
        pourcentage = 100*(classifications_correctes/len(donnees))
        if rep_print == True:
            rep = "Le modèle classifie correctement " + str(pourcentage) + " pourcents des exemples."
            return rep
        elif rep_print == False:
            return pourcentage



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



    def classification_regles(self, rep_print = True):
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

            #...si le nombre de faits partagés est égal au nombre de conditions de la règle (sauf la conclusion, d'où le -1), la règle permet de classifier l'exemple
            if faits_partagés == len(regle) - 1 :
                if rep_print:
                    rep = "La donnée : " + '\n' + str(donnee) + '\n' + " est dans la classe : " + regle[-1] + '\n'
                    regle = regle[:-1]
                    for fait in regle:
                        rep += " Parce que " + fait + '\n'
                    return rep
                else:
                    return regle[-1]
            
        #Parfois aucune règle ne permet de classifier exactement l'exemple
        if rep_print:
            rep = "Pas de classification trouvée grâce aux règles. Néanmoins, selon la méthode classifie, la classe vaut : "
            classification = self.arbre.classifie(self.faits_initiaux, False)
            rep += classification
            return rep
        else:
            return classification
            


    def faits_initialize(self, nom_fichier = None, indice_exemple = None, donnee = None):
        """
        Permet d'initialiser self.faits_initiaux avec une donnée directement (dictionnaire attribut:valeur) ou
        en spécifiant un fichier externe contenant des données et l'indice de l'exemple d'intérêt 
        """
        #On initialse l'attribut avec un nom de fichier et l'indice d'un example
        if donnee == None and nom_fichier != None and indice_exemple != None:
            donnees = self.extract_data(nom_fichier)
            self.faits_initiaux = donnees[indice_exemple][1]
            
        #On initialise l'attribut avec une donnée directement
        elif nom_fichier == None and indice_exemple == None and donnee != None:
            self.faits_initiaux =  donnee
        else:
            print("Erreur: vous avez incorrectement utilisé la méthode")         
        


    def attributs_initialize(self):
        """Parcourt l'arbre dont self.arbre est la racine et initialise les attributs parent, nom et texte 
           de chaque noeud et l'attribut risques en plus pour les noeuds terminaux, cette étape est utile pour 
           la méthode visual_tree et pour la méthode regle_recherche qui utilise l'attribut texte
        """
        if self.arbre.enfants == None:
            return "Erreur, le noeud racine spécifié est vide"

        #On commence l'exploration au niveau du noeud Racine
        noeuds_à_explorer = [self.arbre]
        self.arbre.nom = "Racine"
        self.arbre.texte = "Racine"

        #permet de s'assurer de l'unicité de chaque nom stocké dans l'attribut nom de chaque Noeud (important car chaque nom sera utilisé plus tard comme nom de variable dans visual_tree)
        i = 0

        #Tant qu'on a pas exploré tout l'arbre
        while noeuds_à_explorer:
            noeud_courant = noeuds_à_explorer.pop(-1)

            #Si le noeud a des enfants
            if not(noeud_courant.terminal()):
                for valeur, enfant in noeud_courant.enfants.items():
                    noeuds_à_explorer.append(enfant)
                    enfant.parent = noeud_courant   
                    enfant.nom = noeud_courant.attribut + "_" + valeur + "___" + str(i)  
                    enfant.texte = noeud_courant.attribut + " = " + valeur
                    i+=1
            #Si le noeud est terinal
            elif noeud_courant.terminal(): 
                if noeud_courant.classe() == "0":
                    noeud_courant.risques = "Risques faibles"

                elif noeud_courant.classe() == "1":
                    noeud_courant.risques = "Risques élevés"
                i+=1



    def diagnostic(self, donnee, rep_print = True):
        """ 
        Méthode permettant de fournir à un patient des pistes de traitement qui pourraient faire passer sa classification
        de "risques élevés" à "risques faibles".

        La donnée fournie consigne les informations relatives au patient, c'est un dictionnaire de forme {attribut:valeur}

        Si rep_print = False, la méthode retourne True si un diagnostic a été trouvé et False sinon
        """
        self.faits_initiaux = donnee

        a_pu_être_aide = None

        #On teste tout d'abord si le patient est "à risques ou non"
        classification_patient = self.classification_regles(False)

        if classification_patient == "0":
            rep =  "Le patient n'est pas à risques"
        #Si le patient est à risque
        elif classification_patient == "1":
            rep = "Le patient est à risques" + '\n'
            
            info_patient = []

            #La donnée est transformée sous la forme d'une liste de strings afin de faciliter la comparaison avec les conditions de la règle
            for attribut, valeur in donnee.items():
                info_patient.append(str(attribut + " = " + valeur))

            différences = []
            règles_intéressantes = []
            différences_correspondantes = []

            #On parcourt les règles
            for regle in self.regles:
                #Celles dont la conclusion est optimiste
                if regle[-1] == "0":
                    #Évite que la conclusion soit considérée comme une condition
                    conditions = regle[:-1]
                    for condition in conditions:
                        #On considère les différences entre les conditions de la règle et les info du patient 
                        if condition not in info_patient: 
                            #On vérifie que la règle ne demande pas au patient de changer de sexe ou d'age
                            if condition[0:-4] == "age" or condition[0:-4] == "sex":
                                #Rend la liste des différences trop longue pour que la règle soit condirérée
                                différences += ["", "", ""]
                            else:
                                différences.append(condition)
                    #Si le nombre de différences entre les info du patient et la règle est petit, la règle est intéressante
                    if len(différences) <= 2:

                        règles_intéressantes.append(regle)
                        différences_correspondantes.append(différences)
                
                différences = []
        
            #Aucun diagnostic trouvé
            if len(règles_intéressantes) == 0:
                rep += "Malheureusement, aucune piste de traitement prometeuse n'a été trouvé pour ce patient"
                a_pu_être_aide = False
            #Si au moins une règle intéressante a été trouvée, on propose un diagnostic:
            else:
                rep += "Afin de réduire les risques de maladies cardiaques il faut : " + '\n'
                nbr_diagnostics = len(différences_correspondantes)
                for i,diff in enumerate(différences_correspondantes):
                    #On énumère les attributs dont le patient devrait faire changer la valeur pour guérir
                    for condition in diff:
                        attribut = condition[0:-4]
                        valeur_patient = ""
                        for info in info_patient:
                            if info[0:-4] == attribut:
                                valeur_patient = info[-1]

                        rep += "    - Faire passer la valeur de " + attribut + " de " + valeur_patient + " à " + condition[-1] + '\n'
                    rep += "cela a pu être déduit grâce à la règle : " + str(règles_intéressantes[i]) + '\n'
                    if i < nbr_diagnostics-1:
                        rep += "OU on peut également : " + '\n'
                rep += "Voici les " +  str(nbr_diagnostics) + " solutions à votre disposition."
                a_pu_être_aide = True
        
        if rep_print:
            return rep
        else:
            return a_pu_être_aide


    def nbr_patients_aides(self, nom_fichier):
        """
        Compte parmi les données d'un fichier de test, combien de patients parmi ceux classifiées comme malades
        peuvent bénéficier d'un diagnostic
        """
        donnees = self.extract_data(nom_fichier)

        #Regroupe les patients malades:
        donnees_patients_malades = []
        for donnee in donnees:
            if donnee[0] == "1":
                donnees_patients_malades.append(donnee[1])
        
        nbr_diagnostics = 0
        
        #Cherche un diagnostic pour chaque patient:
        for donnee in donnees_patients_malades:
            #Booléen indiquant si oui ou non un diagnostic a été trouvé
            diagnostic = self.diagnostic(donnee, False)

            if diagnostic == True:
                nbr_diagnostics += 1
        
        rep = "Parmi les " + str(len(donnees)) + " patients, " + str(len(donnees_patients_malades)) 
        rep += " sont malades. Un diagnostic a été trouvé pour " + str(nbr_diagnostics) + " d'entres eux. "
        return rep


    def visual_tree(self): 
        """
        Traduit l'arbre calculé par ID3 sous une forme compréhensible pour la librairie anytree
        puis génère une version visuelle de l'arbre grâce à la librairie graphviz

        On rassemble les informations nécessaires pour créer les noeuds pour anytree 
        dans deux listes de tuples, une pour les noeuds non-terminaux de forme: (nom_noeud, texte, nom_parent)
        et une autre pour les noeuds terminaux de forme: (nom_noeud, risques, nom_parent)

        ATTENTION: la génération des fichiers png nécessite l'utilisation des deux commandes ci-dessous dans 
        l'invite de commande après l'appel de la fonction:

        dot output/arbre.dot -T png -o output/arbre.png
        dot output/graphe.dot -T png -o output/graphe.png
        """

        #Génération du graphique possible seulement si le noeud racine possède des enfants
        if self.arbre.enfants == None:
            return "Erreur : le noeud racine n'a pas d'enfants"

        #Permet d'initialiser les attributs "parent", "texte" et "nom" de chaque noeud sauf la racine
        self.attributs_initialize()

        #inclut les noeuds restants à explorer 
        a_explorer = []
        #Contient des tuples (nom_noeud, texte_à_afficher, nom_parent), chaque élément sous forme de string
        noeuds = []
        #Contient des tuples (nom_noeud, texte_spécifiant_classe, nom_parent), chaque élément sous forme de string
        noeuds_terminaux = []
        #Besoin de générer des noms uniques pour les feuilles
        i = 0
        
        #On traite la racine à part (car elle n'a pas d'attribut parent) et on commence l'exploration au niveau de ses enfants 
        for enfant in self.arbre.enfants.values():
            if not enfant.terminal():
                a_explorer.append(enfant)
            else:
                noeuds.append((enfant.nom, enfant.texte, enfant.parent.nom))
                nom_feuille = "noeud" + str(i)
                noeuds_terminaux.append((nom_feuille, enfant.risques, enfant.nom))
                i+=1
                
        #PARCOURS DE l'ARBRE ET GENERATION DES NOEUDS POUR ANYTREE
        
        while a_explorer:
            #On traite les noeuds pas encore explorés selon un algorithme DFS (last in, first out)
            noeud_courant = a_explorer.pop(0)
            noeuds.append((noeud_courant.nom, noeud_courant.texte, noeud_courant.parent.nom))     
            
            for enfant in noeud_courant.enfants.values():
                
                #Noeud non terminal
                if not(enfant.terminal()):
                    a_explorer.append(enfant)

                #Noeud terminal
                elif enfant.terminal():
                    noeuds.append((enfant.nom, enfant.texte, enfant.parent.nom))
                    nom_feuille = "noeud" + str(i)
                    noeuds_terminaux.append((nom_feuille, enfant.risques, enfant.nom))
                    i+=1
            
        # INITIALISATION DES NOEUDS POUR ANYTREE 
        Racine = Node("Racine")

        #L'initialisation d'un Node est de forme : nom_variable = Node("Texte_du_noeud", parent=_nom_variable_parent)
        for tup in noeuds:
            exec(tup[0] + " = Node(" + '"' + tup[1] + '"' + ", parent = " + tup[2] +")")

        for tup in noeuds_terminaux:
            exec(tup[0] + " = Node(" + '"' + str(tup[1]) + '"'+ ", parent = " + tup[2] +")")

        #Impression dans le terminal de l'arbre
        print(RenderTree(Racine, style=ContRoundStyle()))

        #GENERATION DU GRAPHIQUE PAR GRAPHVIZ ET ANYTREE
        RenderTreeGraph(Racine).to_dotfile("output/graphe.dot")
        UniqueDotExporter(Racine).to_dotfile("output/arbre.dot")



    def tree_setter(self, arbre, advance):
        """
        Setter utile pour la fonction de cross-validation (bonus 2) implémentée dans test_id3.py
        Nécessaire pour permettre l'utilisation de model_eval sur différents arbres
        """

        if advance:
            self.arbre_advance = arbre
        else:
            self.arbre = arbre
    
        
        
        


       
