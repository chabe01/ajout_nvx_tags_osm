import xml.etree.ElementTree as ET
import csv
from traitements import traitements_xml as tx, traitement_fichiers as tf, traitements_annexes as ta

def maj_tags(fichier_osm, fichier_maj, fichier_sortie, sep_fichier_maj = ','):
    """
    Maj à jour des tags en ajoutant de nouveaux à partir du fichier OSM.
    Le fichier maj doit comporter deux colonnes avec une entête : id et nom_cle
    nom_cle est la valeur de la clé associée à chaque valeur de la seconde colonne.

    Par exemple, si on a :
    id,wikidata
    way/1212,Q3441
    way/1213,Q3434
    way/121,4Q343

    Le résultat sera l'ajout d'un champ wikidata avec la valeur associée pour les trois objets de type way

    :param fichier_osm:
    :param fichier_maj:
    :param sep_fichier_maj: séparateur de colonnes du fichier_maj (la virgule par défaut)
    :return:
    """

    cles, dict_nlles_valeurs = recuperer_valeurs_fichier_maj(fichier_maj, sep_fichier_maj)
    root = ET.parse(fichier_osm).getroot()

    nv_root = ajouter_tag_selon_id(dict_nlles_valeurs, cles, root)

    contenu_fichier_sortie = ET.tostring(nv_root).decode('UTF-8') # L'objet est converti en chaîne de caractères

    tf.ecrire_fichier(fichier_sortie, contenu_fichier_sortie) # Écriture du contenu dans le fichier de sortie


def ajouter_tag_selon_id(dict_nlles_valeurs, cles, root):
    """
    Selon l'id donné par type/ref (way/xxxxx, node/xxxxx, relation/xxxx), ajouter un attribut dont la clé est donnée par cle

    :param dict_nlles_valeurs:
    :param root:
    :return:
    """

    # Initalisation du code XML pour OSM
    contenu_fichier_relations = "<?xml version='1.0' encoding='UTF-8'?>"

    # Création de l'objet XML osm
    params_osm = {'version':'0.6','generator':'JOSM'}
    nv_root_osm = tx.creer_element_xml('osm',params_osm)

    types_objets = ['node','way','relation']

    for type_objet in types_objets:
        ajouter_tag_selon_id_et_type(dict_nlles_valeurs, cles, type_objet, root, nv_root_osm)

    return nv_root_osm

def obtenir_attributs_element(elem):
    attributs, attributs_xml = {}, {}
    for ligne in elem.findall('tag'):
        attribut = ligne.attrib
        attributs[attribut['k']] = attribut['v']
        attributs_xml[attribut['k']] = ligne

    return attributs, attributs_xml

def ajouter_ou_pas_attribut(elem, attributs_existants, attributs_xml, params):
    # Créer un nouvel élément xml si l'attribut n'existe pas
    if params['k'] not in attributs_existants.keys():
        nv_elem_fils = tx.creer_element_xml('tag',params)
        tx.ajouter_fils_element_xml(elem,nv_elem_fils)
        elem.set('action','modify')
    # Si l'attribut existe déjà (qu'on veut écraser), on remplace juste la valeur 'v'
    elif params['v'] != attributs_existants[params['k']]:
        attributs_xml[params['k']].set('v',params['v'])
        elem.set('action','modify')
    # Si la valeur est nulle, on fait rien
    elif params['k'] == "":
        return None
    else:
        return None

def ajouter_tag_selon_id_et_type (dict_nlles_valeurs, cles, type_objet, root, nv_root_osm):
    """
    Selon l'id donné par ref ajouter un attribut dont la clé est donnée par cle
    type peut être 'node', 'way' ou 'relation'
    :param dict_nlles_valeurs:
    :param root:
    :return:
    """

    for elem in root.findall(type_objet):
        elem_id = "{}/{}".format(type_objet,elem.get('id'))

        attributs_existants, attributs_xml = obtenir_attributs_element(elem)

        try:
            valeurs_cles = dict_nlles_valeurs[elem_id]
            for i in range(len(cles)):
                params = {'k':cles[i], 'v':valeurs_cles[i]}
                ajouter_ou_pas_attribut(elem, attributs_existants, attributs_xml, params)

            tx.ajouter_fils_element_xml(nv_root_osm,elem)

        except KeyError:
            pass

def recuperer_valeurs_fichier_maj(fichier_maj, sep=','):
    """
    Récupération et structuration des données contenues dans fichier_maj

    :param fichier_maj:
    :return:
    """

    # Lecture du fichier et division du contenu en lignes avec récupération des valeurs selon le séparateur
    with open(fichier_maj, newline='') as csvfile:
        contenu_fichier_brut = csv.reader(csvfile, delimiter=sep)
        contenu_fichier = []
        for ligne in contenu_fichier_brut:
            contenu_fichier.append(ligne)

    # Récupération de la clé (valeur du header de la ou des autres colonnes des attributs)
    cles = contenu_fichier[0][1:]

    dict_nlles_valeurs = {}

    for ligne in contenu_fichier[1:]:
        try:
            ref, valeurs = ligne[0], ligne[1:]
            dict_nlles_valeurs[ref] = valeurs
        except ValueError:
            pass

    return cles, dict_nlles_valeurs


if __name__ == '__main__':
    fichier_osm = '/Users/charlybernard/Desktop/velib.osm'
    fichier_maj = '/Users/charlybernard/Desktop/test.csv'
    fichier_sortie = '/Users/charlybernard/Desktop/velib_out.osm'

    maj_tags(fichier_osm, fichier_maj, fichier_sortie)
