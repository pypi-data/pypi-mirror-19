pdml2flow-elasticsearch |PyPI version|
======================================

*Saves `pdml2flow <https://github.com/Enteee/pdml2flow>`__ output in
elasticsearch*

+-----------+--------------------------+-----------------------------+
| Branch    | Build                    | Coverage                    |
+===========+==========================+=============================+
| master    | |Build Status master|    | |Coverage Status master|    |
+-----------+--------------------------+-----------------------------+
| develop   | |Build Status develop|   | |Coverage Status develop|   |
+-----------+--------------------------+-----------------------------+

Prerequisites
-------------

-  `pdml2flow <https://github.com/Enteee/pdml2flow>`__
-  `python <https://www.python.org/>`__:
-  3.4
-  3.5
-  3.5-dev
-  nightly
-  `pip <https://pypi.python.org/pypi/pip>`__

Installation
------------

.. code:: shell

        $ sudo pip install pdml2flow-elasticsearch

Configuration
-------------

+------------------------+-----------------------------+
| Environment variable   | Description                 |
+========================+=============================+
| ES\_HOST               | Elasticsearch hostname      |
+------------------------+-----------------------------+
| ES\_PORT               | Elasticsearch port number   |
+------------------------+-----------------------------+
| ES\_INDEX              | Elasticsearch index name    |
+------------------------+-----------------------------+
| ES\_TYPE               | Elasticsearch type name     |
+------------------------+-----------------------------+

Example
-------

.. |PyPI version| image:: https://badge.fury.io/py/pdml2flow-elasticsearch.svg
   :target: https://badge.fury.io/py/pdml2flow-elasticsearch
.. |Build Status master| image:: https://travis-ci.org/Enteee/pdml2flow-elasticsearch.svg?branch=master
   :target: https://travis-ci.org/Enteee/pdml2flow-elasticsearch
.. |Coverage Status master| image:: https://coveralls.io/repos/github/Enteee/pdml2flow-elasticsearch/badge.svg?branch=master
   :target: https://coveralls.io/github/Enteee/pdml2flow-elasticsearch?branch=master
.. |Build Status develop| image:: https://travis-ci.org/Enteee/pdml2flow-elasticsearch.svg?branch=develop
   :target: https://travis-ci.org/Enteee/pdml2flow-elasticsearch
.. |Coverage Status develop| image:: https://coveralls.io/repos/github/Enteee/pdml2flow-elasticsearch/badge.svg?branch=develop
   :target: https://coveralls.io/github/Enteee/pdml2flow-elasticsearch?branch=develop
