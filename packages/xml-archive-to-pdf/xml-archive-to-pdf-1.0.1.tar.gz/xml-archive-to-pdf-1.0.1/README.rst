xml-archive-to-pdf
==================

.. image:: https://travis-ci.org/unistra/xml-archive-to-pdf.svg?branch=master
    :target: https://travis-ci.org/unistra/xml-archive-to-pdf
    :alt: Build

.. image:: http://coveralls.io/repos/unistra/xml-archive-to-pdf/badge.png?branch=master
    :target: http://coveralls.io/r/unistra/xml-archive-to-pdf?branch=master
    :alt: Coverage

.. image:: https://img.shields.io/badge/python-3.4-blue.svg
    :target: https://www.python.org/download/releases/3.4.0/
    :alt: Python 3.4

Transformation d'un fichier xml de type *unistra:archive* en fichier pdf

Installation
------------

.. code-block:: bash

    pip install xml-archive-to-pdf

Usage
-----

.. code-block:: bash

    xml-archive-to-pdf -i tests/data/pathfinder_1.xml -o /tmp/pathfinder_1.pdf --logo tests/data/logo.png

Documentation
-------------

Structuration d'un fichier xml de type *unistra:archive*
********************************************************

L'objectif est de pouvoir générer simplement un fichier pdf en se basant sur un fichier xml conforme à la norme *unistra:archive*.
En amont, il faudra s'assurer que le fichier xml soit validé par un schéma xsd et qu'il contient toutes les informations nécessaires à la fabrication du pdf.

On aura principalement :

* Des blocs séparés par des titres
* Des clés avec un intitulé parlant
* Des valeurs


Exemple d'un fichier xml
************************

.. code-block:: xml

    <?xml version="1.0" encoding="UTF-8"?>
    <!-- Racine du fichier, id et source sont optionnels, le name correspond au titre -->
    <personnage xmlns="fr:unistra:di:archive:pathfinder:v1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="fr:unistra:di:archive:pathfinder:v1 pathfinder_v1.xsd"
        id="1" source="pathfinder" name="document récapitulatif du personnage 1 de pathfinder">
        <!-- Affiche le sous-titre de l'état civil -->
        <etat-civil name="son état civil">
            <!-- Affichage de clés/valeurs -->
            <nom>Sombre-crâne</nom>
            <age name="son âge">20</age>
            <!-- Nouveau bloc avec un sous-titre -->
            <classes name="classes et niveaux">
                <!-- Ici on affiche le sous-titre de name -->
                <classe name="Première classe">
                    <nom>Barbare</nom>
                    <niveau>3</niveau>
                </classe>
                <!-- Ici name est vide, donc ça affiche un titre vide -->
                <classe name="">
                    <nom>Prêtre combattant</nom>
                    <niveau>1</niveau>
                </classe>
                <!-- Lorsqu'il n'y a pas d'attribut name, on affiche le nom du tag. Ici classe -->
                <classe>
                    <nom>Moine</nom>
                    <niveau>2</niveau>
                </classe>
            </classes>
        </etat-civil>
        <!-- Element de style tableau -->
        <armes style="table" name="Liste des armes">
            <arme>
                <nom>cimeterre</nom>
                <type>à deux mains</type>
                <portee name="portée">3</portee>
                <degat name="dégât">7</degat>
            </arme>
            <arme>
                <nom>arc</nom>
                <type>à distance</type>
                <portee name="portée">8</portee>
                <degat name="dégât">2</degat>
            </arme>
            <arme>
                <nom>épée</nom>
                <type>à une main</type>
                <portee name="portée">5</portee>
                <degat name="dégât">3</degat>
            </arme>
        </armes>
    </personnage>

Légende de l'exemple
********************

attributs
#########

* name : intitulé parlant qui servira de label/titre à la place du nom du tag
* style : style d'un bloc

  * table: affichage sous forme d'un tableau


Résultat
********

* `Fichier pdf de l'exemple <https://github.com/unistra/xml-archive-to-pdf/blob/master/tests/data/pathfinder_1.pdf>`_
