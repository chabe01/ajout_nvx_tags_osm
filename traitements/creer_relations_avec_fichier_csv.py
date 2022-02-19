import xml.etree.ElementTree as ET
from traitements import traitements_xml as tx, traitement_fichiers as tf, traitements_annexes as ta


def creer_relation(tags, id):
    """

    :param donnees: dictionnaire dont les clés sont les clés de la relation et les valeur sont les valeurs de la relation
    :type  donnees: dict
    :param id: faux id temporaire créé avant sa sauvegarde
    :type  id: int

    :return: relation créée selon les tags désirés
    :rtype: xml.etree.ElementTree.Element
    """

    # Création de la relation sans aucun tag
    relation_params = {'id': '-{}'.format(id), 'action': 'modify',
                       'visible': 'true'}  # Attributs de la relation (pas les tags)
    relation = tx.creer_element_xml('relation', relation_params)

    # Création et ajout des tags dans la relation
    for key in tags:
        tag_params = {'k': key, 'v': tags[key]}
        nouveau_tag = tx.creer_element_xml('tag', tag_params)
        tx.ajouter_fils_element_xml(relation, nouveau_tag)

    return relation

def creer_relations(tags_par_relation, version='0.6', generator='JOSM'):
    """
    Creer plusieurs relations à partir d'une liste dont chaque élément est un dictionnaire comportant les tags pour une relation

    :param tags_par_relation:
    :type  tags_par_relation: list of dict
    :param version: paramètre de version pour le fichier comportant toutes les relations, 0.6 par défaut
    :type  version: str
    :param generator: paramètre de generator pour le fichier comportant toutes les relations, JOSM par défaut
    :type  generator: str

    :return:
    """

    toutes_relations_params = {'version': version, 'generator': generator}
    toutes_relations = tx.creer_element_xml('osm', toutes_relations_params)

    for i in range(len(tags_par_relation)):
        relation = creer_relation(tags_par_relation[i], i+1) #id est l'index + 1 pour ne pas avoir de 0
        tx.ajouter_fils_element_xml(toutes_relations, relation)

    return toutes_relations

def creer_relations_avec_fichier_csv(fichier_csv,sep=','):
    """
    Créer des relations à partir d'un fichier de configuration. Chaque ligne (à part la première) représente une relation
    et chaque élément de la ligne est une valeur d'un tag dont la clé est donnée par l'élément associé en première ligne

    Si le fichier est :
    type,name,country
    associatedStreet,Route des Coudes,France
    associatedStreet,Allée la Levée,Royaume-Uni

    Le résultat final est deux relations :
    - relation_1 : type=associatedStreet, name=Route des Coudes, country=France
    - relation_2 : type=associatedStreet, name=Allée la Levée, country=Royaume-Uni

    :param fichier_csv: fichier CSV comportant les données pour créer les relations
    :type  fichier_csv: str
    :param sep: séparateur des valeurs du fichier CSV, une virgule par défaut
    :type  sep: str

    :return: ensemble des relations créées respectant la syntaxe d'un fichier OSM pour JOSM
    :rtype: xml.etree.ElementTree.Element
    """

    contenu_fichier = tf.lire_fichier(fichier_csv)
    lignes_fichier = contenu_fichier.split("\n") # Séparer les lignes du fichier

    en_tete = lignes_fichier[0].split(sep) # Obtenir l'en-tête
    tags_par_relation = []

    # Lire toutes les lignes excepté l'en tête
    for ligne in lignes_fichier[1:]:
        if ligne != '': # Ignorer ce traitement si la ligne est vide
            tags_relation = {}
            elements_ligne = ligne.split(sep)
            for i in range(len(elements_ligne)):
                cle, valeur = en_tete[i], elements_ligne[i]
                tags_relation[cle] = valeur

            tags_par_relation.append(tags_relation)

    relations = creer_relations(tags_par_relation)

    return relations

if __name__ == '__main__':
    fichier_csv = '/Users/charlybernard/Downloads/test.csv'
    relations = creer_relations_avec_fichier_csv(fichier_csv)
    relations_et = ET.ElementTree(relations)
    relations_et.write("/Users/charlybernard/Downloads/test.osm")