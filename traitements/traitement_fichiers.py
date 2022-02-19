"""
Ce script permet de faire des traitements de base sur des fichiers, c'est-à-dire les lire ou en écrire
"""

import json
import re

def lire_fichier(nom_fichier: str) -> str:
    """
    Lire un fichier dont le chemin est donbé par nom_fichier
    :param nom_fichier: nom (chemin) du fichier à lire
    :return: contenu du fichier
    """
    fichier = open(nom_fichier,"r")
    contenu_fichier = fichier.read()
    fichier.close()

    return contenu_fichier


def ecrire_fichier(nom_fichier: str ,contenu_fichier: str) -> None:
    """
    Écrire du contenu donné par contenu_fichier dans un fichier dont le chemin est nom_fichier
    :param nom_fichier: nom (chemin) du fichier à écrire
    :param contenu_fichier: contenu du fichier à écrire
    :return:
    """
    fichier = open(nom_fichier,"w")
    fichier.write(contenu_fichier)
    fichier.close()


def construire_dict_abreviations(fichier_abreviations: str, sep:str=',') -> dict:
    """
    À partir d'un fichier, construire un dictionnaire dont les clés sont les abréviations et les valeurs sont les noms entiers

    Fichier doit être du type :
    Abreviation_1,Nom_1
    ...
    Abreviation_n,Nom_n

    :param fichier_abreviations:
    :param sep:
    :return:
    """

    # Lire le contenu du fichier
    contenu_fichier = lire_fichier(fichier_abreviations)

    # Initialisation du dictionnaire des abréviations
    dict_abreviations = {}

    for ligne in contenu_fichier.split("\n"):
        abre_nom = ligne.split(sep) # Liste contenant l'abréviation et le nom

        try:
            dict_abreviations[abre_nom[0]] = abre_nom[1] # Ajout de l'association clé-valeur dans le dictionnaire
        except:
            pass

    return dict_abreviations

def recuperer_donnees_maj(fichier_maj: str,sep:str=",") -> tuple:
    """
    À partir d'un fichier à deux colonnes dont la première est une donnée déjà présente dans les relations
    et la seconde est celle qu'il faut ajouter, la fonction crée un dictionnaire dont la clé est la donnée de la 1re
    colonne et la valeur est celle de la seconde.

    Le fichier doit contenir un header qui donne la clé attributaire OSM du tag qu'elle décrit.
    Par exemple, si la première colonne donne des codes FANTOIR et des id de Wikidata, le header sera : "ref:FR:FANTOIR,wikidata"

    :param fichier_maj:
    :param sep:
    :return:
    """

    # Lire le contenu du fichier
    contenu_fichier = lire_fichier(fichier_maj)

    # Initialisation du dictionnaire des abréviations
    dict_donnees = {}

    # Récupération des lignes du fichier
    lignes_fichier = contenu_fichier.split("\n")

    # Données du header
    cle_1,cle_2 = lignes_fichier[0].split(sep)[0:2]

    for ligne in lignes_fichier[1:]:
        try:
            cle,valeur = ligne.split(sep)[0:2]
            dict_donnees[cle] = valeur
        except ValueError:
            pass

    return cle_1,cle_2,dict_donnees

def creer_fichier_geojson(nom_fichier_adresses:str,sep:str=","):
    """
    À partir du fichier des adresses, créer un fichier geojson des adresses
    :param nom_fichier_adresses:
    :return:
    """

    # Lire le fichier et récupérer le header
    contenu_fichier_entree = lire_fichier(nom_fichier_adresses).split('\n')
    header = contenu_fichier_entree[0].split(sep)  # Les colonnes sont séparées par un séparateur défini en entrée de la fonction

    # Récupération de la position des indices des coordonnées
    try:
        indice_lon = header.index('lon')
        indice_lat = header.index('lat')

    except ValueError:
        print("Fichier Geojson non créé...")
        return None # Si les colonnes désirées n'existent pas, la fonction s'arrête

    liste_adresses = []

    for ligne in contenu_fichier_entree[1:]:
        valeurs = ligne.split(sep)  # Récupération des valeurs de l'adresse dans la liste
        # Récupération de la valeur de rep et mise en forme

        # Dictionnaire liée à l'adresse courante et ajout des éléments
        dict_adresse = {}
        dict_adresse["type"] = "feature"
        dict_adresse["geometry"] = { "type": "Point", "coordinates": [float(valeurs[indice_lon]), float(valeurs[indice_lat])]}

        # Ajout des propriétés dans le dictionnaire properties (sans les coordonnées)
        properties = {}
        for i in range(len(valeurs)):
            if i not in [indice_lat,indice_lon]:
                properties[header[i]] = valeurs[i]

        dict_adresse["properties"] = properties

        # Ajout du dictionnaire dans la liste des adresses
        liste_adresses.append(dict_adresse)

    # Contenu final du geojson
    contenu_geojson = {"type":"FeatureCollection",
                       "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:OGC:1.3:CRS84" } },
                       "features": liste_adresses}

    # Écrire le contenu dans un fichier geojson
    nom_geojson_adresses = re.sub(r'(\..{0,}$)', "", nom_fichier_adresses) + ".geojson"
    with open(nom_geojson_adresses, 'w', encoding='utf-8') as fp:
        json.dump(contenu_geojson, fp, ensure_ascii=False)
