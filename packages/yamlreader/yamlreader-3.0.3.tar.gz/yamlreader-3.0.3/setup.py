#!/usr/bin/env python

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'yamlreader',
        version = '3.0.3',
        description = '''Merge YAML data from given files, dir or file glob''',
        long_description = '''.. image:: https://travis-ci.org/ImmobilienScout24/yamlreader.png?branch=master
   :alt: Travis build status image
   :align: left
   :target: https://travis-ci.org/ImmobilienScout24/yamlreader

==========
yamlreader
==========
Merge YAML data from a directory, a list of files or a file glob. With a
directory, the YAML files (`*.yaml`) are sorted alphabetically. The YAML
files are expected to contain a complex key-value structure and merged
with the following rules:

* lists get appended
* hashes get merged by key
* scalars (numbers, strings) are overwritten
* everything else will fail

The purpose is to allow several YAML files instead of a single YAML file. We
use it to help our software read configuration data from an arbitrary amount
of YAML files instead of a single YAML file.

Read the unit test to see some examples.

Building and Installation
=========================
Using pip
---------
**yamlreader** is available with ``pip``:
::

    pip install yamlreader

Manual build and installation
-----------------------------
If you want to make changes or use e.g. ``fpm`` for packaging this, you need to
prepare the development environment to make further steps.

Prepare the source
~~~~~~~~~~~~~~~~~~
::

    git clone https://github.com/ImmobilienScout24/yamlreader.git
    cd yamlreader
    virtualenv venv
    source venv/bin/activate
    pip install pybuilder
    pyb install_dependencies

Running tests
~~~~~~~~~~~~~
::

    pyb verify

Generating a setup.py
~~~~~~~~~~~~~~~~~~~~~
::

    pyb
    cd target/dist/yamlreader-<VERSION>
    ./setup.py <whatever you want>

Running
=======
The package installs a command line script ``yamlreader`` that can be used to
read one or many YAML files and dump the merge result as a YAML document.

Use it in your software
=======================
Wherever you had been using the ``safe_load`` function of
`PyYAML <http://pyyaml.org/>`_ to read a single YAML file you can use
the ``yamlreader.yaml_load`` function as a replacement to read all ``*.yaml``
files in a directory::

    from yamlreader import yaml_load

    defaultconfig = {
            "loglevel" : "error",
            "some" : "value"
    }

    config = yaml_load("/etc/myapp", defaultconfig)

yaml_load
---------
::

    def yaml_load(source,defaultdata=None):
        """merge YAML data from files found in source

        Always returns a dict. The YAML files are expected to contain some kind of
        key:value structures, possibly deeply nested. When merging, lists are
        appended and dict keys are replaced. The YAML files are read with the
        yaml.safe_load function.

        source can be a file, a dir, a list/tuple of files or a string containing
        a glob expression (with ?*[]).

        For a dir all *.yaml files will be read in alphabetical order.

        defaultdata can be used to initialize the data.
        """
''',
        author = "Schlomo Schapiro",
        author_email = "schlomo.schapiro@immobilienscout24.de",
        license = 'Apache License 2.0',
        url = 'https://github.com/ImmobilienScout24/yamlreader',
        scripts = [],
        packages = ['yamlreader'],
        py_modules = [],
        classifiers = [
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6'
        ],
        entry_points = {
            'console_scripts': ['yamlreader=yamlreader:__main']
        },
        data_files = [],
        package_data = {},
        install_requires = [
            'PyYAML',
            'six'
        ],
        dependency_links = [],
        zip_safe=True,
        cmdclass={'install': install},
    )
