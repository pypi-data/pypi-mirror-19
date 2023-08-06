Import de thésaurus SKOS
========================

Lorsqu'il est lancé par l'interface web, l'import de thésaurus SKOS ne peut
utiliser les optimisations qui deviennent nécessaires dès que le thésaurus est
de taille conséquente (plus d'une centaine de concepts). En effet ces
optimisations nécessitent que l'import soit effectué sans que d'autres
connexions à la base de données soient actives (ce qui implique donc de stopper
le serveur web pendant ce temps).

Pour importer un fichier SKOS RDF sans que celui-ci soit rattaché à une source de données (cette
dernière permettant de conserver la source et donc de synchroniser les données plus tard), vous
pouvez utiliser la commande 'skos-import' : ::

  cubicweb-ctl skos-import saem fichier.rdf


Pour déclencher l'import initial ou la synchronisation de données SKOS RDF dont l'URL a été
spécifiée par l'ajout d'une source dans l'interface web, vous pouvez utiliser la commande
'source-sync' : ::

  cubicweb-ctl source-sync saem <nom de la source>

Ces deux exemples supposent que votre instance se nomme "saem" et que vous avez coupé l'interface
web au préalable (``cubicweb-ctl stop saem``).
