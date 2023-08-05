=======
CFDILib 
=======

.. image:: https://badge.fury.io/py/cfdilib.svg
    :target: https://badge.fury.io/py/cfdilib

.. image:: https://travis-ci.org/Vauxoo/cfdilib.svg?branch=master
    :target: https://travis-ci.org/Vauxoo/cfdilib

.. image:: https://codecov.io/gh/Vauxoo/cfdilib/branch/master/graph/badge.svg?token=wcRGfPzSDy
    :target: https://codecov.io/gh/Vauxoo/cfdilib

.. image:: https://landscape.io/github/Vauxoo/cfdilib/master/landscape.svg?style=flat
   :target: https://landscape.io/github/Vauxoo/cfdilib/master
   :alt: Code Health

Library to xml documents based on XSD files to manage situations where you need to sign such
documents with a third party, then given a simple dictionary and a jinja2 template you will be
able to generate such documents with almos 0 logic.

* Free software: Vauxoo Licence (LGPL-v3)
* Documentation: https://vauxoo.github.io/cfdilib

Features
--------

* TODO


=======
History
=======

latest
------

* XMl for Journal Items: Assigned id by the next:

Atributo requerido para expresar el número único de identificación de la
póliza. El campo deberá contener la clave o nombre utilizado por el
contribuyente para diferenciar, el tipo de póliza y el número correspondiente.
En un mes ordinario no debe repetirse un mismo número de póliza con la clave o
nombre asignado por el contribuyente. 

0.3.3
------

* Refactor of the code for cache the temp downloaded files.
* Fixed minor lint problems to improve the readability of the code.

latest
------

* Refactor of the code for cache the temp downloaded files.
* Fixed minor lint problems to improve the readability of the code.

0.3.1
-----

* Refactiring the validation approach to use a proper way and not be sticked to
  an specific lxml version

0.3.0
------

* Electronic accounting ready.

  * CoA.
  * Moves.
  * Balance


0.1.0 (2016-1-22)
------------------

* First release on PyPI.


