import xml.etree.ElementTree as ET
from traitement import creer_relations_avec_fichier_csv as crafc, ajouter_elements_relation as aer


def main(fichier_csv, fichier_elements_osm, fichier_sortie_osm, dict_correspondance,
         types_elements=['node', 'way', 'relation'], filtre_tags=[]):
    """
    À partir d'un fichier csv, créer des relations, et ajouter des éléments qui sont dans fichier_elements_osm. Pour lier
    les éléments aux relations, dict_correspondance est utilisé.
    filtre_tags est utilisé pour sélectionner uniquement certains éléments. Par exemple, si filtre_tags = [highway, ref],
    les éléments sélectionnés sont ceux qui ont les clés highway et ref

    :param fichier_csv:
    :param fichier_elements_osm:
    :param fichier_sortie_osm:
    :param dict_correspondance:
    :return:
    """

    root_relations = crafc.creer_relations_avec_fichier_csv(fichier_csv)
    root_elements = ET.parse(fichier_elements_osm).getroot()

    # Ajout des éléments
    aer.maj_relations_avec_elements(root_elements, root_relations, dict_correspondance, types_elements, filtre_tags)

    # Écriture du fichier de sortie
    root_relations_et = ET.ElementTree(root_relations)
    root_relations_et.write(fichier_sortie_osm)


if __name__ == '__main__':
    fichier_csv = '/Users/charlybernard/Downloads/relations_rd_77.csv'
    fichier_osm = '/Users/charlybernard/Downloads/rd_77.osm'
    fichier_out = '/Users/charlybernard/Downloads/out.osm'
    dict_correspondance = {'ref': 'ref'}
    types_elements = ['way']
    filtre_tags = []

    main(fichier_csv, fichier_osm, fichier_out, dict_correspondance, types_elements=['node', 'way', 'relation'],
         filtre_tags=[])
