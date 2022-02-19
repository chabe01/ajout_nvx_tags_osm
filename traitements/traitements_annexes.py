import re
import traitements.traitements_xml as tx
import xml.etree.ElementTree as ET

def supprimer_accents_majuscules(expression):
    """
    Suppression de tous les accents et majuscules l'expression
    :param expression:
    :return:
    """

    if expression is None:
        return None

    nlle_exp = expression.lower().replace("-", " ")
    nlle_exp = re.sub("’", "'", nlle_exp)
    nlle_exp = re.sub("(é|è|ê|ë)", "e", nlle_exp)
    nlle_exp = re.sub("(â|à|ä)", "a", nlle_exp)
    nlle_exp = re.sub("(ù|ü|û)", "u", nlle_exp)
    nlle_exp = re.sub("ç", "c", nlle_exp)
    nlle_exp = re.sub("(î|ï)", "i", nlle_exp)
    nlle_exp = re.sub("(ô|ö)", "o", nlle_exp)
    nlle_exp = re.sub("ÿ", "y", nlle_exp)
    nlle_exp = re.sub("œ", "oe", nlle_exp)
    nlle_exp = re.sub("æ", "ae", nlle_exp)

    return nlle_exp

def faire_corrections_bon_sens(expression):
    """
    Faire des correction de bon sens
    :param expression:
    :return:
    """

    # Autres corrections de bon sens
    nlle_exp = re.sub('iere','ière',expression)
    nlle_exp = re.sub('yere','yère',nlle_exp)
    nlle_exp = re.sub('llere','llère',nlle_exp)
    nlle_exp = re.sub('Saint ','Saint-',nlle_exp)
    nlle_exp = re.sub('Sainte ','Sainte-',nlle_exp)
    nlle_exp = re.sub('Saints ','Saints-',nlle_exp)
    nlle_exp = re.sub('Saintes ','Saintes-',nlle_exp)
    nlle_exp = re.sub('theque','thèque',nlle_exp)
    nlle_exp = re.sub('metre','mètre',nlle_exp)
    nlle_exp = re.sub('ee$','ée',nlle_exp)
    nlle_exp = re.sub('ee $','ée ',nlle_exp)
    nlle_exp = re.sub('ees$','ées',nlle_exp)
    nlle_exp = re.sub('ees $','ées ',nlle_exp)

    return nlle_exp

def supprimer_termes_inutiles(expression):
    """
    Supprimer les articles et autres termes inutiles de l'expression (du type EN, ET, LE, LA...)
    :param expression:
    :return:
    """

    nlle_expression = expression

    termes_inutiles = ['le','la','les','du','de','des','et','en','au','à','a','aux']
    termes_inutiles_apostrophes = ['l','d','l’','d’']

    for terme in termes_inutiles:
        nlle_expression = re.sub('( {} | {}$|^{} )'.format(terme,terme,terme)," ",nlle_expression) # Suppresion du terme inutile

    for terme in termes_inutiles_apostrophes:
        nlle_expression = re.sub('{}\''.format(terme),"",nlle_expression)

    nlle_expression = re.sub('( {1,}$|^ {1,})',"",nlle_expression) # Suppression d'éventuels espaces en début et fin d'expression

    return nlle_expression

def modifier_nombres(expression,dict_abreviations_nombres):
    """
    Unifier les nombres cardinaux et ordinaux qui peuvent différer selon les sources.
    On peut trouver 'Rue du 11 Novembre' tout comme 'Rue du Onze Novembre'
    De même, on peut avoir "Rue Albert Ier", "Rue Albert Premier" ou "Rue Albert 1er"

    :param expression:
    :return:
    """

    nlle_exp = expression

    exp_ordinaux = '(ieme|iemes|eme|emes|me|mes|er|ers|ere|eres|re|res|d|de|des|nd|nde|ndes)' # Termes pouvant être utlisés comme abréviations d'ordinaux
    exp_genre_nombre = '(e|s|es){0,1}' # Lorsque l'ordinal est écrit en toute lettre, cette variable est faite pour gérer le féminin et le pluriel

    # Remplacement des nombres écrit en lettre par des chiffres
    for key in dict_abreviations_nombres.keys():
        nlle_exp = re.sub('( {}{} | {}{}$|^{}{} )'.format(key,exp_genre_nombre,key,exp_genre_nombre,key,exp_genre_nombre),' {} '.format(dict_abreviations_nombres[key]),nlle_exp)
        nlle_exp = re.sub('( {}{} | {}{}$|^{}{})'.format(key,exp_ordinaux,key,exp_ordinaux,key,exp_ordinaux),' {}e '.format(dict_abreviations_nombres[key]),nlle_exp)

    # Suppression des suffixes du type 'eme', 'ième' pour les remplacer par 'e'
    # Par exemple, '3ième' devient '3e'
    for i in range(10):
        nlle_exp = re.sub(
            '( {}{} | {}{}$|^{}{} )'.format(i, exp_ordinaux, i, exp_ordinaux, i, exp_ordinaux),
            ' {}e '.format(i), nlle_exp)

    return nlle_exp

def formater_expression(expression,dict_abreviations_nombres=None):
    """
    Formatter l'expression, c'est-à-dire supprimer les accents et les termes inutiles
    :param expression:
    :return:
    """

    if expression is None:
        return None

    nlle_expression = supprimer_accents_majuscules(expression)
    nlle_expression = supprimer_termes_inutiles(nlle_expression)

    if dict_abreviations_nombres is not None:
        nlle_expression = modifier_nombres(nlle_expression,dict_abreviations_nombres)

    return nlle_expression

def reecrire_nom_voie(nom_voie,dict_abreviations_voies,dict_abreviations_autres):
    """
    Réécrire de manière propre le nom de la voie de sorte à supprimer les abréviations et les lettres majuscules inutiles
    :param nom_voie:
    :param dict_abreviations_voies:
    :param dict_abreviations_autres:
    :return:
    """

    # Chaque terme de la liste est un mot du nom de la voie
    termes_nom_voie = nom_voie.split(" ")

    # Décoller l'abrévation de la voie du reste (lorsque l'abréviation fait 4 caractères)
    if len(termes_nom_voie[0]) >= 4:
        abreviation = termes_nom_voie[0][0:4]
        reste_premier_terme = termes_nom_voie[0][4:]
    else:
        abreviation, reste_premier_terme = termes_nom_voie[0],""

    # Initialisation du nom amélioré de la voie en commançant par son type
    # Dans ce cas-là, l'abréviation est bien séparée
    try:
        nv_nom_voie = "{} ".format(dict_abreviations_voies[abreviation])
        termes_nom_voie = [abreviation, reste_premier_terme] + termes_nom_voie[1:]

    # Dans le cas où l'abréviation n'existe pas, on recolle les termes
    except:
        termes_nom_voie = [abreviation + reste_premier_terme] + termes_nom_voie[1:]
        # Le premier terme est reformaté (avec accents...)
        try:
            premier_terme = dict_abreviations_autres[termes_nom_voie[0]]
        except:
            premier_terme = termes_nom_voie[0]

        nv_nom_voie = "{} ".format(premier_terme.capitalize())

    # Lecture des mots formant le nom, on exclut le premier mot qui est le type de la voie
    for mot in termes_nom_voie[1:]:
        mot = mot.upper()
        if mot != "":
            try:
                nv_mot = dict_abreviations_autres[mot]
            except:
                nv_mot = reconstituer_expression(mot,dict_abreviations_autres)

            nv_nom_voie += "{} ".format(nv_mot)

    nom_final = nv_nom_voie[:-1] #Suppression du dernier espace inutile
    nom_final = nom_final.replace("' ","'") # Suppression des espaces entre une apostrophe et l'espace d'après

    nom_final = faire_corrections_bon_sens(nom_final)
    return nom_final

def reecrire_nom_voie_sans_abreviation(nom_voie,dict_abreviations_autres):
    """
    Réécrire de manière propre le nom de la voie
    :param nom_voie:
    :param dict_abreviations_autres:
    :return:
    """

    # Chaque terme de la liste est un mot du nom de la voie
    termes_nom_voie = nom_voie.split(" ")

    nv_nom_voie = ""

    # Lecture des mots formant le nom, on exclut le premier mot qui est le type de la voie
    for mot in termes_nom_voie:
        mot = mot.upper()
        if mot != "":
            try:
                nv_mot = dict_abreviations_autres[mot]
            except:
                nv_mot = reconstituer_expression(mot,dict_abreviations_autres)

            nv_nom_voie += "{} ".format(nv_mot)

    nom_final = nv_nom_voie[:-1] #Suppression du dernier espace inutile
    nom_final = nom_final.replace("' ","'") # Suppression des espaces entre une apostrophe et l'espace d'après

    nom_final = faire_corrections_bon_sens(nom_final)
    return nom_final

def reconstituer_expression(expression,dict_abreviations_autres):
    """
    Reconstituer une expression selon une syntaxe donnée si elle possède des apostrophes ou des tirets

    :param expression:
    :return:
    """

    nlle_exp = ""
    termes_exp = [elem.split("-") for elem in expression.split("'")]

    for i in range(len(termes_exp)):
        for j in range(len(termes_exp[i])):
            terme = termes_exp[i][j].capitalize()

            try:
                terme = dict_abreviations_autres[terme.upper()] # Modification du terme s'il est dans le dictionnaire des abréviations
            except:
                pass

            if j != len(termes_exp[i]) - 1:
                nlle_exp += terme + "-"
            else:
                nlle_exp += terme

    return nlle_exp

def associer_nouvel_attribut_selon_autre(relation,cle_rel_select,cle_a_ajouter,dict_valeurs,dict_abreviations_nombres):
    """
    Dans une relation, on a plusieurs combinaisons cle=valeur. Selon une des cle=valeur, on veut ajouter une nouvelle combinaison.

    Par exemple, en fonction de la cle ref:FR:FANTOIR, on pourrait ajouter une valeur associée à Wikidata.
    dict_valeurs serait alors un dictionnaire dont les clés sont des codes ref:FR:FANTOIR et les valeurs sont des pages Wikidata

    :param relation:
    :param cle_rel_select:
    :param cle_a_ajouter:
    :param dict_valeurs:
    :return:
    """

    # Ajouter le nouvel attribut que si la clé à ajouter n'existe pas
    if not tx.valeur_tag_existe(relation,cle_a_ajouter):
        valeur_cle_rel_select = tx.recuperer_valeur_tag(relation,cle_rel_select) # Récupérer une valeur de la relation selon la clé cle_rel_select

        # Récupération de la valeur à ajouter dans le dictionnaire si elle existe
        try:
            # Formattage de l'expression pour un meilleur matching
            if cle_rel_select in ('name','addr:city','addr:street'):
                valeur_cle_rel_select = formater_expression(valeur_cle_rel_select,dict_abreviations_nombres)

            valeur_a_ajouter = dict_valeurs[valeur_cle_rel_select]
            param_ajout = {cle_a_ajouter:valeur_a_ajouter}
            maj_attributs_relation(relation,param_ajout)

        except KeyError:
            pass

def maj_attributs_relation(relation,params):
    """
    Ajouts de nouveaux éléments tag dans la relation
    :param relation:
    :param params:
    :return:
    """

    # Arrêter le processus s'il n'y a rien à ajouter
    if len(params.keys()) == 0:
        return None

    # Ajout des nouveaux éléments si le dictionnaire n'est pas vide
    for key in params.keys():
        dict_params = {"k":key,"v":params[key]}
        elem_tag = tx.creer_element_xml('tag',dict_params)
        tx.ajouter_fils_element_xml(relation,elem_tag)

    # Ajout d'un attribut à la relation pour indiquer qu'elle a été modifiée
    attributs_modif = {"action":"modify"}
    tx.ajouter_atrributs_element_xml(relation,attributs_modif)


def maj_attributs_relations(root,cle_ref,cle_ajout,dict_donnees,dict_abreviations_nombres):
    """
    Mettre à jour les relations de type=associatedStreet

    :param root:
    :param cle_ref:
    :param cle_ajout:
    :param dict_donnees:
    :return:
    """

    # Initalisation du code XML pour OSM
    contenu_fichier_relations = "<?xml version='1.0' encoding='UTF-8'?>"

    # Création de l'objet XML osm
    params_osm = {'version': '0.6', 'generator': 'JOSM'}
    osm = tx.creer_element_xml('osm', params_osm)

    # Mettre à jour les relations et l'ajouter dans le fichier de sortie
    for relation in root.findall('relation'):
        associer_nouvel_attribut_selon_autre(relation,cle_ref,cle_ajout,dict_donnees,dict_abreviations_nombres)
        tx.ajouter_fils_element_xml(osm,relation)

    # Les données sont écrites dans le fichier de sortie
    contenu_fichier_relations += ET.tostring(osm).decode('UTF-8')

    return contenu_fichier_relations

def intersections_listes(listes):
    liste_intersection = listes[0]

    for liste in listes[1:]:
        liste_intersection_temp = []
        for elem in liste_intersection:
            if elem in liste:
                liste_intersection_temp.append(elem)
        liste_intersection = liste_intersection_temp

    return liste_intersection