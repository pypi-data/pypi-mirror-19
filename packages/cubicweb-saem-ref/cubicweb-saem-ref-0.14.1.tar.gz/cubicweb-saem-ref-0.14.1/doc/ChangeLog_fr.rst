Historique des révisions
========================

**0.13**

SEDA :

Changement majeur lié à l'utilisation du cube seda développé avec le SIAF sur la base du modèle SEDA
2, en lieu et place du modèle développé dans le référentiel. Pour le moment, uniquement les profils
"simplifiés" du cube seda sont visibles, et non les profils SEDA 2 complet. Ce changement entraîne :

* quelques éléments supplémentaires dans le modèle SEDA supporté (qu'il reste à exporter en XSD/RNG
  0.2/1.0),

* une interface utilisateur un peu différente,

* un support de l'export des profils au format RNG, ainsi qu'en version SEDA 2,

* uniquement des unités d'archives comme composant SEDA, plus de *data object* / document.

A noter que l'aide à la saisie "globale" (i.e. au niveau du profil) était avant transmise via le
champ *commentaire* du seda 0.2. C'est maintenant une annotation comme pour les autres, et on peut
décrire des commentaires comme les autres champs SEDA.

EAC :

Utilisation du cube eac extrait du référentiel pour utilisation dans le cadre du projet France
Archives. Ceci a permis d'avoir dans cette livraison l'implémentation du champ 'OtherRecordId' qui a
été financé par le SIAF.


OAI :

* Il faut maintenant obligatoirement indiquer le "metadata prefix" lors
des échanges oai pmh ;

* Dans le cas des profils, il y a maintenant les formats `seda02xsd`, `seda02rng`, `seda1rng` et
  `seda2rng` ;

* Les notices d'autorités sont exposés en EAC via le format `eac`.


RDF :

* Utilisation d'URL pérenne dans les exports RDF, i.e. n'incluant pas d'élément possiblement
  changeant de l'entité, et si possible en se basant sur l'identifiant ark.


**0.12**

Interface utilisateur :

* Optimisation pour minimiser le nombre de requêtes des pages principales (#12136865)

* Déploiement WSGI - devrait améliorer le support des requêtes concurrentes  (#12136865)

EAC :

* Séparation d'agent en une partie fonctionnelle (`OrganizationUnit` et `Agent`) et une partie
  archivistique EAC (`AuthorityRecord`) (#12140367).

SEDA :

* Amélioration de l'arbre SEDA (#12059534) :

  - drag and drop désactivé pour les anonymes

  - suppression des requêtes synchrone, ce qui devrait améliorer l'utilisabilité globale

  - tentative d'amélioration de l'affichage des hiérarchie en supprimant la marge sur les feuilles de l'arbre

* Import multiples #12205200


Interopérabilité :

* Modification du XSD exporté :
  - plus d'attribut `type` sur les éléments définis "en-ligne",
  - utilisation d'`extension` pour les éléments avec un contenu textuel et des attributs.

* Les *setspecs* OAIPMH ``agent:kind:<KIND NAME>`` ont été supprimés du fait de
  la dichotomie ``Agent`` / ``OrganizationUnit``.

* Le setSpec OAI-PMH ``agent`` a été renommée en ``organizationunit`` (incluant tous les setSpecs
  sous-jacents tels que ``organizationunit:role:control`` par exemple).

* Un setSpecs OAI-PMH ``agent`` a été introduit pour permettre de moissonner les entités de type
  ``Agent``.


**0.11.0**

Interopérabilité :

* Ajout d'un préfix 'ark:/' devant la valeur du champ 'identifier' de l'en-tête OAI-PMH, qu'il
  convient de retirer pour construire les setSpec qui eux n'ont pas changé (#11831203).

* Ajout dans le RDF d'un agent des relations hiérarchiques et d'association avec l'ontologie
  Organization du W3C (#11668412).

* Correction de l'export XSD des profils SEDA pour produire du XSD valide et non le format
  spécifique à Agape (#3606843)


Interface utilisateur :

* Charte graphique (#11754074).

* Ajout des types d'entités Collectivité (Authority) et Autorité d'assignement de nom ARK
  (ARKNameAssigningAuthority) afin de contrôler la collectivité responsable d'un agent et l'autorité
  d'assignement de nom à utiliser pour la génération des identifiants ARK (#11855091).

* Correction de l'autocomplétion pour éviter des propositions incohérentes (#11884489).

* Affichage uniquement des agents de types personnes dans la liste déroulante contact référent
  (#11867467).

* Lancement automatique de la recherche après sélection d'une proposition de l'autocomplétion
  (#11884492).

* Optimisation de l'affichage des arbres de concept sur les vocabulaire : temps d'affichage divisé
  par deux (#11884230).

* Suppression de l'action "Copier" sur les agents (#11716529).

* Correction de l'import des objets-données ou des unités documentaires SEDA (#11785516).

* Correction de l'affichage de l'arbre "Elément du profil SEDA" pour les objets données ou des
  unités documentaires (#11785524).

* Navigation plus cohérente pour les objets-données et unités documentaires des unités d'archive
  SEDA (#11557857)

* Utilisation de l'annotation comme titre des objets-données SEDA (#3471036).

* Utilisation d'un vocabulaire pour les durées de conservation SEDA (#3466081).

* Affichage correct des données contenant des accents importées via EAC (#11664020).


EAC :

* Meilleure gestion de l'import/export des paragraphes (#11987275) et des liens (#11664008) EAC.

* Import des balises <generalContext> (#3511427) et <objectXMLWrap> (#3381087).

* Import des fichiers sans éléments <authorizedForm> (#11716516).

* Nommage des fichiers exportés sur la base de l'identifiant ARK (#11664003).

* Corrections pour la validation de l'EAC exporté (#11663901).


Déploiement :

* Mise à disposition d'une recette Salt pour l'installation sur CentOS 6 ou 7, incluant la mise à
  disposition d'un entrepôt de paquets CentOS 7 (#11884390).



**0.10.0**

* affichage des (sous)-concepts sous forme d'une liste paginée plutôt qu'un arbre s'il y a plus
  de 500 concepts à afficher (#2974227, #3350215)

* amélioration de synchronisation de source depuis l'interface : aide en ligne, warning plutôt
  qu'erreur en cas de définition multi-lingues non supportée, outil pour import de thésaurus de
  taille importante (#3392144, #3349339)

* problème d'interface empêchant la liaison de concept équivalent si le vocabulaire est publié
  (#5603390)

* possibilité de mise à jour des vocabulaires contrôlés publiés : possibilité d'ajout de nouveaux
  concepts et d'ajout / suppression de libellés (#11578206)

* import des balises EAC mandates et des sous-balises mandate (#3381084)

* import des balises EAC occupations et des sous-balises occupation (#3381034)

* export au format XML EAC des fiches agents (#3239716)

* état des lieux des balises non implémentés du schéma EAC (#11543984)

* changement de la gestion des vocabulaires sources : dans l'interface, soit on sélectionne un
  vocabulaire et un champ permet de sélectionner un concept de ce vocabulaire via auto-complétion,
  soit on peut saisir du texte libre (#3512232, #3511423)

* on n'affiche pas les agents liés à des utilisateurs dans les listes déroulantes (#3384078)

* on n'affiche pas les agents non publiés dans les listes déroulantes (#3507748)

* intégration basique de la charge graphique développé pour le blog saem, dont notamment le logo
  (#11520162)

*  plus d'incohérence dans l'interface des agents quand on édite les rôles archivistiques (#3510158)

* correction fautes d'orthographe (#11544090, #11557853)

* suppression de la relation `useProfile` dans 'export RDF, on peut utiliser les *sets* OAI pour
  obtenir cette information (#3507873)

* ajout des relations chronolique en utilisant `dcterms:isReplacedBy` (partie de #3477127)

* suppression de la gestion de connecteur vers alfresco et asalae (#3478851)

* amélioration de la gestion des démonstrateurs : sentry, supervision, docker reproductible
  (#11509296)


**0.9.1**

* l'export RDF d'un agent de type service versant n'inclut plus la description complète de son
  service archive, uniquement son URL

* L'attribut foaf:type d'un agent de type contact dans l'export RDF d'un agent est bien foaf:Person

* Plus d'agent dans l'état brouillon exporté sur certains set OAI

* On ne peut plus supprimer des éléments d'un profil publié

* Corrections de plantages sur agent avec lieu sans adresse ou sur certains set OAI avec resumption
  token

* Corrections / amélioration de label

**0.9.0**

* ajout des concepts en tant que set specifiers OAI-PMH de premier niveau

  la requête `oai?verb=ListSets` renvoie maintenant des set avec le préfixe
  `concept` du type :

    * `concept`
    * `concept:in_scheme:saemref-test/000002219`

  ce dernier résultat permet de filter les concepts d'un vocabulaire
  particulier via son identifiant

* correction du problème de dates pour l'OAI-PMH : toutes les dates sont maintenant en UTC
  tant au niveau des résultats retournés que des restrictions de requête via
  `from`/`until` ; on retourne les informations de fuseaux horaires (le
  suffixe `Z` dans le cas de l'UTC).

* ajout d'attribut à la balise OAI-PMH pour la définition des espaces des noms
  notamment et du schéma de validation

* utilisation d'identifiant ARK pour les profils dans OAI-PMH

* gestion des entités supprimées dans OAI-PMH par ajout d'une balise <header status="deleted">

* web service d'attribution d'ARK (il faut être authentifié) ::

    POST /ark/
    Accept: application/json

  Exemples de réponse (JSON) ::

    [{'ark': '12345/ext-000000001'}]

    [{'error': 'This service is only accessible using POST.'}]

    [{'error': 'This service requires authentication.'}]

* le service versant et service archive associé d'un profil ne sont plus inclus dans l'export SEDA XSD
