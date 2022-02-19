from traitements import ajout_tag_selon_id as atsi
import argparse
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Mettre à jour des données OSM via un fichier texte')
    parser.add_argument('--osm', help = "Fichier OSM où des mises à jour doivent être faites")
    parser.add_argument('--maj', help = "Fichier texte définissant les mises à jour")
    parser.add_argument('--out', help = "Fichier de sortie")
    parser.add_argument('--sep', help = "Séparateur (1 caractère) dans le fichier de mise à jour (optionel et ',' par défaut)")

    args = parser.parse_args(sys.argv[1:])
    fichier_osm = args.osm
    fichier_maj = args.maj
    fichier_sortie = args.out
    sep_fichier_maj = args.sep

    if type(sep_fichier_maj) is not str or len(sep_fichier_maj) != 1:
        sep_fichier_maj = ","

    atsi.maj_tags(fichier_osm, fichier_maj, fichier_sortie, sep_fichier_maj)
