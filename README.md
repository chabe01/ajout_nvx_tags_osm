# ajout_tag_selon_id
Ajouter un (ou plusieurs) tags à des objets OSM (node, way, relation) stockés dans un fichier `osm` à partir d'un fichier `csv`.

Le fichier `csv` doit respecter une syntaxe bien définie :
* un header renseignant le nom des tags ;
* les autres lignes commencent par l'`id` osm (`[node]|[way]|[relation]/value`) suivi des valeurs des tags associés à ceux défnis dans le header ;
* les éléments sont séparés par un élément séparateur d'un seul caractère, `,` est la valeur par défaut.

Exemple :
`id,name,wikidata`<br/>
`relation/11827653,Rue de Rivoli,Q141747`<br/>
`node/17807753,Paris,Q90`<br/>
`way/643131004,Avenue des Champs-Élysées,`

Pour lancer le programme, deux fichiers sont nécessaires :
* le fichier `csv` précédemment présenté ;
* le fichier `osm` qui contient les objets OSM définis dans le fichier `csv`. Si un des éléments ne s'y trouve pas, il ne sera pas mis à jour

La commande est la suivante (variable `sep` est facultative) :
`$ python3 main.py --maj=[fichier_csv] --osm=[fichier_osm] --out=[fichier_osm_sortie] --sep=[sep]`
