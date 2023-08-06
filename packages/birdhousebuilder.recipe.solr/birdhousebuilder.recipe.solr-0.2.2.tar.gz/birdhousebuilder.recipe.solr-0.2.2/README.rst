****************************
birdhousebuilder.recipe.solr
****************************

.. image:: https://travis-ci.org/bird-house/birdhousebuilder.recipe.solr.svg?branch=master
   :target: https://travis-ci.org/bird-house/birdhousebuilder.recipe.solr
   :alt: Travis Build

Introduction
************

``birdhousebuilder.recipe.solr`` is a `Buildout`_ recipe to install and configure `Solr`_ using `Anaconda`_.
``Solr`` will be deployed as a `Supervisor`_ service.

This recipe is used by the `Birdhouse`_ project.

.. _`Buildout`: http://buildout.org/
.. _`Anaconda`: http://continuum.io/
.. _`Supervisor`: http://supervisord.org/
.. _`Solr`: https://lucene.apache.org/solr/
.. _`Birdhouse`: http://bird-house.github.io/


Usage
*****

The recipe requires that Anaconda is already installed.
You can use the buildout option ``anaconda-home`` to set the prefix for the anaconda installation.
Otherwise the environment variable ``CONDA_PREFIX`` (variable is set when activating a conda environment) is used as conda prefix.

It installs the ``solr`` package from a conda channel in a conda environment defined by ``CONDA_PREFIX``.
The intallation folder is given by the ``prefix`` buildout option.
It deploys a `Supervisor`_ configuration for Solr in ``${prefix}/etc/supervisor/conf.d/solr.conf``.
Supervisor can be started with ``${prefix}/etc/init.d/supervisord start``.

By default ``Solr`` will be available on http://localhost:8983/solr.

The recipe depends on ``birdhousebuilder.recipe.conda`` and ``birdhousebuilder.recipe.supervisor``.

Supported options
=================

The recipe supports the following options:

**anaconda-home**
  Buildout option pointing to the root folder of the Anaconda installation. Default: ``$HOME/anaconda``.

**hostname**
   The hostname of the ``Solr`` service (nginx). Default: ``localhost``.

**http-port**
   The http port of the ``Solr`` service (nginx). Default: ``8983``.

**java-home**
    Path to your JAVA_HOME. By default it uses the java installation from conda (package ``openjdk``).
    Default: ``${prefix}``.


Example usage
=============

The following example ``buildout.cfg`` installs ``Solr`` with Anaconda::

  [buildout]
  parts = solr

  [solr]
  recipe = birdhousebuilder.recipe.solr
  hostname = localhost
  http-port = 8983
