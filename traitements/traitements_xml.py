import xml.etree.ElementTree as ET

def creer_element_xml(nom_elem,params):
    """
    Créer un élément de la relation qui va donner un des attributs.
    Par exemple, pour ajouter le code FANTOIR pour une relation, il faut que le code XML soit <tag k='ref:FR:FANTOIR' v='9300500058T' />"
    Pour cela, il faut le nom de l'élément (ici tag) et un dictionnaire de paramètres nommé param qui associe chaque clé à une valeur (ici
    {'k':'ref:FR:FANTOIR',  'v'='9300500058T'}

    :param nom_elem:
    :type  nom_elem: str
    :param params:
    :type  params: dict
    :return: élément XML désiré
    :rtype: xml.etree.ElementTree.Element
    """

    # Initialisation de l'objet XML
    elem = ET.Element(nom_elem)

    ajouter_atrributs_element_xml(elem, params)

    return elem

def ajouter_atrributs_element_xml(elem,attributs):
    """
    Ajouter des atrributs dans un élément xml
    :param elem:
    :param attributs:
    :return:
    """

    # Ajout des paramètres un par un
    for key in attributs.keys():
        elem.set(key, attributs[key])


def ajouter_fils_element_xml(elem,elem_fils):
    """
    Ajouter un élément fils à l'élément xml
    :param elem:
    :param attributs:
    :return:
    """

    elem.insert(0, elem_fils)

def valeur_tag_existe(elem,cle_valeur):
    """
    Détermine si la valeur associée à cle_valeur dans la relation existe déjà pour éviter de la modifier
    :param elem:
    :param cle_valeur:
    :return:
    """

    # Recherche de tous les éléments tag de l'objet elem
    for item in elem.findall('tag'):
        if item.get("k") == cle_valeur:
            return True

    return False

def recuperer_valeur_tag(elem,cle_valeur):
    """
    Dans OSM, les attributs d'une relation sont dans les objets tag de l'objet XML de la relation.
    Récupérer la valeur associée à la clé cle_valeur

    :param elem:
    :param cle_valeur:
    :return:
    """

    # Recherche de tous les éléments tag de l'objet elem
    for item in elem.findall('tag'):
        if item.get("k") == cle_valeur:
            return item.get("v")

    return None

def recuperer_toutes_valeurs_tag(elem):
    """
    Récupérer toutes les valeurs des tags de l'élement
    :param elem:
    :return:
    """

    valeurs_tag = {}

    # Recherche de tous les éléments tag de l'objet elem
    for item in elem.findall('tag'):
        try:
            cle, valeur = item.get("k"), item.get("v")
            valeurs_tag[cle] = valeur
        except:
            pass

    return valeurs_tag



if __name__ == '__main__':
    test = '<relation action="modify" id="-102236" visible="true"><tag k="ref:FR:FANTOIR" v="AZZAZAZA" /><member ref="362303309" role="street" type="way" /></relation>'
    test_xml = ET.fromstring(test)

