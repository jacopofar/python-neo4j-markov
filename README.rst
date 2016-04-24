===============================
Neo4j Markov Chains
===============================

<!-- .. image:: https://img.shields.io/pypi/v/neo4j_markov_chains.svg
        :target: https://pypi.python.org/pypi/neo4j_markov_chains

.. image:: https://img.shields.io/travis/jacopofar/neo4j_markov_chains.svg
        :target: https://travis-ci.org/jacopofar/neo4j_markov_chains

.. image:: https://readthedocs.org/projects/neo4j_markov_chains/badge/?version=latest
        :target: https://readthedocs.org/projects/neo4j_markov_chains/?badge=latest
        :alt: Documentation Status
        -->


A module to store and use Markov chains in a Neo4j 3 instance.

* Free software: ISC license
<!-- * Documentation: https://neo4j_markov_chains.readthedocs.org. -->

Features
________

* Support multiple concurrent instances, each action is a transition taking advantage of  Neo4j ´MERGE ... ON CREATE ... ON MATCH´ functionality
* Efficient next-status random choice using Neo4j reducer

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
