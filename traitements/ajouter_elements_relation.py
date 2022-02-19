import xml.etree.ElementTree as ET
from traitements import traitements_xml as tx, traitement_fichiers as tf, traitements_annexes as ta


def selectionner_elems_selon_tags(root, liste_tags, types_osm):
    """

    :param root:
    :param liste_tags:
    :type  liste_tags: list
    :param types_osm: type d'objet OSM : node et/ou way et/ou relation
    :type  types_osm: list of str
    :return: liste des éléments sélectionnés
    """

    elems = []

    # Lire tous les objets de type type_osm
    for type_osm in types_osm:
        for elem in root.findall(type_osm):
            if element_selectionnable(elem, liste_tags):
                elems.append(elem)

    return elems


def element_selectionnable(elem, liste_tags):
    """
    Voir si l'élément est sélectionnable, c'est-à-dire s'il possède tous les tags qui sont dans la liste

    :param elem: élement osm (node, way, relation)
    :type  elem: xml.etree.ElementTree.Element
    :param liste_tags: liste des tags qu'on veut que l'élément ait
    :type  liste_tags: list of str
    :return: True si l'élément est sélectionnable, False sinon
    :rtype: bool
    """

    tags = [x.get('k') for x in elem.findall('tag')]

    for tag in liste_tags:
        if tag not in tags:
            return False

    return True


def obtenir_tags_relations(relations, liste_tags):
    """
    Pour chaque tag de liste_tags, obtenir un dictionnaire dont la clé est un valeur associée au tag et la valeur est
    une liste des relations qui ont la combinaison cle=valeur

    Par exemple, pour une liste de relations des communes de l'Ain et tag postal_code, le dictionnaire serait :
    {'postal_code': {'01380':[rel_1, rel_2], '01290':[rel_3]}} où rel_1 est une relation qui possède postal_code=01380

    Ceci se faisant sur une liste de tags, le dictionnaire possède autant d'éléments que de tags

    :param relations: liste des relations
    :type  relations: list of xml.etree.ElementTree.Element
    :param liste_tags: liste des tags
    :type  liste_tags: list of str
    :return:
    """

    # Initialisation du dictionnaire des tags
    tags_relations = {x: {} for x in liste_tags}

    for relation in relations:
        valeurs_tag_relation = tx.recuperer_toutes_valeurs_tag(relation)
        for tag in liste_tags:
            try:
                valeur = valeurs_tag_relation[tag]
                try:
                    tags_relations[tag][valeur].append(relation)
                except KeyError:
                    tags_relations[tag][valeur] = [relation]

            except KeyError:
                pass

    return tags_relations


def ajouter_membres_dans_relations(elements, relations, dict_correspondance):
    """
    Ajouter des éléments (node, way, relation) situés dans dict_elements pour les ajouter dans des relations de dict_relations.

    :param elements: liste des éléments qui peuvent être ajoutés dans des relations
    :type  elements: list of xml.etree.ElementTree.Element
    :param relations: liste des relations où il faut ajouter des éléments
    :type  relations: list of xml.etree.ElementTree.Element
    :param dict_correspondance:
    :type  dict_correspondance: dict
    :return:
    """

    tags_relations = obtenir_tags_relations(relations, list(dict_correspondance.values()))

    for elem in elements:
        relations_pour_element = obtenir_relations_pour_element(elem, tags_relations, dict_correspondance)
        for relation in relations_pour_element:
            ajouter_membre_relation(relation, elem, role='')


def ajouter_membre_relation(relation, elem, role=''):
    """
    Ajouter le membre elem dans la relation
    :param elem:
    :param relation:
    :return:
    """

    membre_params = {'type': elem.tag, 'ref': elem.get('id'), 'role': role}
    membre = tx.creer_element_xml('member', membre_params)
    tx.ajouter_fils_element_xml(relation, membre)


def obtenir_relations_pour_element(element, tags_relations, dict_correspondance):
    """
    Poru l'élement element donné en entrée, obtenir la liste des relations pour lesquelles l'élément doit être membre
    :param element:
    :type  element: xml.etree.ElementTree.Element
    :param tags_relations:
    :type  tags_relations: dict
    :param dict_correspondance:
    :type  dict_correspondance: dict
    :return:
    """
    tags_element = tx.recuperer_toutes_valeurs_tag(element)

    # Liste qui va comporter des sous listes qui elles-mêmes comporteront des relations
    listes_relations = []

    for key in dict_correspondance:
        try:
            tag_element = tags_element[key]
            relations_tag = tags_relations[dict_correspondance[key]][tag_element]  # Liste de relations
            listes_relations.append(relations_tag)
        except KeyError:
            return []  # Arrêter le processus si un des éléments n'existe pas

    relations_pour_elem = ta.intersections_listes(listes_relations)

    return relations_pour_elem


def maj_relations_avec_elements(root_elements, root_relations, dict_correspondance,
                                types_elements=['node', 'way', 'relation'], filtre_tags=[]):

    # Lister les éléments qui peuvent être membres de relations et lister ces relations-là
    liste_elements = selectionner_elems_selon_tags(root_elements, filtre_tags, types_elements)
    liste_relations = root_relations.findall('relation')

    # Ajouter les éléments en fonction de l'appariement donné par dict_correspondance
    ajouter_membres_dans_relations(liste_elements, liste_relations, dict_correspondance)


if __name__ == '__main__':
    nom_fichier_elements = '/Users/charlybernard/Downloads/01343.osm'
    nom_fichier_relations = '/Users/charlybernard/Downloads/test.osm'
    nom_fichier_out = '/Users/charlybernard/Downloads/test_out.osm'

    root_elements = ET.parse(nom_fichier_elements).getroot()
    root_relations = ET.parse(nom_fichier_relations).getroot()

    dict_correspondance = {'ref': 'ref'}

    maj_relations_avec_elements(root_elements, root_relations, dict_correspondance,
                                types_elements=['node', 'way', 'relation'], filtre_tags=[])

    # Écriture du fichier de sortie
    root_relations_et = ET.ElementTree(root_relations)
    root_relations_et.write(nom_fichier_out)
