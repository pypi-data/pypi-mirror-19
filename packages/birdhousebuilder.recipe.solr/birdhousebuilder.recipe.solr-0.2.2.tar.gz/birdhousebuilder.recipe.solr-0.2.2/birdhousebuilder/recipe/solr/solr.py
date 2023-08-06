# -*- coding: utf-8 -*-

"""Recipe solr"""

import os
import pwd
import logging
from mako.template import Template

import zc.recipe.deployment
from zc.recipe.deployment import Configuration
from zc.recipe.deployment import make_dir
import birdhousebuilder.recipe.conda
from birdhousebuilder.recipe import supervisor

templ_solr_env = Template(filename=os.path.join(os.path.dirname(__file__), "templates", "solr.in.sh"))
templ_log4j = Template(filename=os.path.join(os.path.dirname(__file__), "templates", "log4j.properties"))
templ_solr_core = Template(filename=os.path.join(os.path.dirname(__file__), "templates", "core.properties"))
templ_jetty_context = Template(
    filename=os.path.join(os.path.dirname(__file__), "templates", "solr-jetty-context.xml"))


def make_dirs(name, user, mode=0o755):
    etc_uid, etc_gid = pwd.getpwnam(user)[2:4]
    created = []
    make_dir(name, etc_uid, etc_gid, mode, created)


class Recipe(object):
    """This recipe is used by zc.buildout.
    It installs solr from conda and setups solr configuration and a supervisor service."""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        b_options = buildout['buildout']

        self.name = options.get('name', name)
        self.options['name'] = self.name

        self.logger = logging.getLogger(self.name)

        # deployment layout
        def add_section(section_name, options):
            if section_name in buildout._raw:
                raise KeyError("already in buildout", section_name)
            buildout._raw[section_name] = options
            buildout[section_name]  # cause it to be added to the working parts

        self.deployment_name = self.name + "-solr-deployment"
        self.deployment = zc.recipe.deployment.Install(buildout, self.deployment_name, {
            'name': "solr",
            'prefix': self.options['prefix'],
            'user': self.options['user'],
            'etc-user': self.options['etc-user']})
        add_section(self.deployment_name, self.deployment.options)

        self.options['etc-prefix'] = self.options['etc_prefix'] = self.deployment.options['etc-prefix']
        self.options['var-prefix'] = self.options['var_prefix'] = self.deployment.options['var-prefix']
        self.options['etc-directory'] = self.options['etc_directory'] = self.deployment.options['etc-directory']
        self.options['lib-directory'] = self.options['lib_directory'] = self.deployment.options['lib-directory']
        self.options['log-directory'] = self.options['log_directory'] = self.deployment.options['log-directory']
        self.options['run-directory'] = self.options['run_directory'] = self.deployment.options['run-directory']
        self.options['cache-directory'] = self.options['cache_directory'] = self.deployment.options['cache-directory']
        self.prefix = self.options['prefix']

        # conda packages
        self.options['env'] = self.options.get('env', '')
        self.options['pkgs'] = self.options.get('pkgs', 'solr')
        self.options['pip'] = self.options.get('pip', 'pysolr')
        self.options['channels'] = self.options.get('channels', 'defaults birdhouse')
        self.conda = birdhousebuilder.recipe.conda.Recipe(self.buildout, self.name, {
            'env': self.options['env'],
            'pkgs': self.options['pkgs'],
            'channels': self.options['channels']})
        self.options['conda-prefix'] = self.options['conda_prefix'] = self.conda.options['prefix']

        # java options
        self.options['java_home'] = self.options['java-home'] = self.options.get(
            'java-home', self.options['conda-prefix'])

        # jetty options
        self.options['hostname'] = options.get('hostname', 'localhost')
        self.options['http-port'] = self.options['http_port'] = options.get('http-port', '8983')

        # solr options
        self.options['core'] = options.get('core', 'birdhouse')
        self.solr_home = self.options['lib-directory']
        self.options['solr-home'] = self.options['solr_home'] = self.solr_home
        self.options['core-directory'] = self.options['core_directory'] = os.path.join(
            self.solr_home, self.options.get('core'))
        self.options['core-conf-directory'] = self.options['core_conf_directory'] = os.path.join(
            self.options['core-directory'], 'conf')

        # make folders
        make_dirs(self.options['core-directory'], self.options['user'], mode=0o755)
        make_dirs(self.options['core-conf-directory'], self.options['etc-user'], mode=0o755)
        make_dirs(os.path.join(self.options['core-directory'], 'data'), self.options['user'], mode=0o755)

    def install(self, update=False):
        installed = []
        if not update:
            installed += list(self.deployment.install())
        installed += list(self.conda.install(update))
        installed += list(self.install_jetty_context())
        installed += list(self.install_solr_xml())
        installed += list(self.install_solr_env())
        installed += list(self.install_log4j())
        installed += list(self.install_core_properties())
        installed += list(self.install_core_config())
        installed += list(self.install_core_schema())
        installed += list(self.install_supervisor(update))
        return installed

    def install_jetty_context(self):
        text = templ_jetty_context.render(**self.options)
        config = Configuration(self.buildout, 'solr-jetty-context.xml', {
            'deployment': self.deployment_name,
            'directory': os.path.join(self.options['conda-prefix'],
                                      'opt', 'solr', 'server', 'contexts'),
            'text': text})
        return [config.install()]

    def install_solr_xml(self):
        config = Configuration(self.buildout, 'solr.xml', {
            'deployment': self.deployment_name,
            'directory': self.solr_home,
            'file': os.path.join(os.path.dirname(__file__), "templates", "solr.xml")})
        return [config.install()]

    def install_solr_env(self):
        text = templ_solr_env.render(**self.options)
        config = Configuration(self.buildout, 'solr.in.sh', {
            'deployment': self.deployment_name,
            'directory': self.solr_home,
            'text': text})
        return [config.install()]

    def install_log4j(self):
        text = templ_log4j.render(**self.options)
        config = Configuration(self.buildout, 'log4j.properties', {
            'deployment': self.deployment_name,
            'directory': self.solr_home,
            'text': text})
        return [config.install()]

    def install_core_properties(self):
        text = templ_solr_core.render(**self.options)
        config = Configuration(self.buildout, 'core.properties', {
            'deployment': self.deployment_name,
            'directory': self.options['core-directory'],
            'text': text})
        return [config.install()]

    def install_core_config(self):
        text = templ_solr_core.render(**self.options)
        config = Configuration(self.buildout, 'solrconfig.xml', {
            'deployment': self.deployment_name,
            'directory': self.options['core-conf-directory'],
            'file': os.path.join(os.path.dirname(__file__), "templates", "solrconfig.xml")})
        return [config.install()]

    def install_core_schema(self):
        text = templ_solr_core.render(**self.options)
        config = Configuration(self.buildout, 'schema.xml', {
            'deployment': self.deployment_name,
            'directory': self.options['core-conf-directory'],
            'file': os.path.join(os.path.dirname(__file__), "templates", "schema.xml")})
        return [config.install()]

    def install_supervisor(self, update=False):
        solr_dir = os.path.join(self.options['conda-prefix'], 'opt', 'solr')
        solr_env = os.path.join(self.solr_home, 'solr.in.sh')
        script = supervisor.Recipe(
            self.buildout,
            self.name,
            {'prefix': self.options['prefix'],
             'user': self.options.get('user'),
             'etc-user': self.options['etc-user'],
             'program': 'solr',
             'command': '{0}/bin/solr start -f'.format(solr_dir),
             'environment': 'SOLR_INCLUDE="{0}"'.format(solr_env),
             'directory': solr_dir,
             'stopwaitsecs': '10',
             'killasgroup': 'true',
             'stopasgroup': 'true',
             'stopsignal': 'KILL',
             })
        return script.install(update)

    def update(self):
        return self.install(update=True)


def uninstall(name, options):
    pass
