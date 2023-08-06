Installation
============

Configuration des entrepôts yum
-------------------------------

Télécharger et installer les RPMs suivants (ils n'installent que des fichiers
.repo dans ``/etc/yum.repos.d/``) :

* https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm
* http://yum.postgresql.org/9.4/redhat/rhel-6-x86_64/pgdg-centos94-9.4-1.noarch.rpm

::

    rpm -ivh epel-release-latest-6.noarch.rpm
    rpm -ivh pgdg-centos94-9.4-1.noarch.rpm


Créer ``/etc/yum.repos.d/logilab-extranet-BRDX.repo`` avec le contenu suivant,
en remplaçant ``LOGIN`` et ``PASSWORD`` par le nom d'utilisateur et le mot de
passe de l'extranet Logilab :

::

    [logilab-extranet-BRDX]
    name=Logilab Extranet BRDX EPEL $releasever - $basearch
    baseurl=https://LOGIN:PASSWORD@extranet.logilab.fr/static/BRDX/rpms/epel-$releasever-$basearch
    enabled=1
    gpgcheck=0


Installation des paquets nécessaires
------------------------------------


Ensuite installer :

::

    yum install cubicweb-saem-ref
    yum install postgresql94-contrib
    yum install postgresql94-plpython
    yum install postgresql94-server
    yum install mailcap # pour /etc/mime.types


Configuration du serveur PostgreSQL
-----------------------------------

Créer et démarrer un *cluster* PostgreSQL

::

    service postgresql-9.4 initdb
    service postgresql-9.4 start

En tant qu'utilisateur ``postgres`` (par exemple ``su - postgres``),
créer un nouveau compte d'accès à Postgres :

::

    createuser --superuser --login --pwprompt cubicweb

De retour en ``root``, éditer le fichier ``/var/lib/pgsql/9.4/data/pg_hba.conf``
pour donner les droits d'accès à l'utilisateurs ``cubicweb`` fraichement créé :

::

    local   all   cubicweb    md5


.. warning::

    L'ordre des directives de ce fichier est important. La directive concernant
    l'utilisateur ``cubicweb`` doit précéder celles déjà présentes dans le
    fichier. Dans le cas contraire, elle sera ignorée.

Enfin, on relance PostgreSQL pour qu'il prenne en compte les modifications :

::

    service postgresql-9.4 reload

Pour s'assurer du bon fonctionnement de PostgreSQL et du rôle ``cubicweb``, la
commande suivante doit afficher le contenu du *cluster* sans erreur :

::

    psql -U cubicweb -l


Création de l'instance
----------------------

Une fois le cube saem_ref et ses dépendances installées, il reste à créer une
instance de celui-ci :

::

  cubicweb-ctl create saem_ref saem_ref

.. note ::

    La phase finale de création prend quelques minutes, afin de remplir la base
    avec quelques données nécessaires au bon fonctionnement de l'application.

* Laisser le choix par défaut à toutes les questions ;

* Choisir un login / mot de passe administrateur sécurisé (admin/admin est une
  mauvaise idée, nous recommandons d'installer le paquet ``pwgen`` et de
  générer un mot de passe aléatoire avec la commande ``pwgen 20``).

Puis à la lancer :
::

  cubicweb-ctl start saem_ref

L'instance est désormais lancée et disponible sur le port 8080.


Mise à jour de l'instance
=========================

Lors qu'une nouvelle version est livrée, il faut commencer par mettre à jour les paquets installés
sur le système :

::

  yum check-update
  yum update

Il est possible que ``check-update`` ne détecte pas les paquets à mettre jour
du fait d'un problème de cache. Dans ce cas, on peut nettoyer le cache (pour
l'entrepôt ``logilab-extranet-BRDX``) de cette façon :

::

  yum --disablerepo='*' --enablerepo=logilab-extranet-BRDX clean expire-cache


Puis il reste à mettre à jour l'instance CubicWeb. Celle-ci sera automatiquement stoppée (et
redémarrée le cas échéant), il y aura donc une interruption de service pendant cette opération.

::

  cubicweb-ctl upgrade saem_ref

Cette commande pose un certain nombre de questions, auxquelles il faut toujours répondre par oui (en
tapant 'y' ou Entrée directement).


