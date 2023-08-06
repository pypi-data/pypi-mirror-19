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
        name = 'karellen-sqlite',
        version = '0.0.3',
        description = 'Karellen Sqlite Extensions',
        long_description = 'Karellen Sqlite Extensions\n==========================\n\n|Gitter chat|\n\nAbout\n-----\n\nThis project contains `Karellen <https://www.karellen.co/karellen/>`__\n`Sqlite <https://docs.python.org/3/library/sqlite3.html>`__ extensions\nto the standard Python SQLite3 module.\n\nThese extensions are verified to work with Python 3.x (x >= 3) on Linux\nx86\\_64 and have been verified to work with GA and Debug builds of\nCPython. Any CPython ABI-compliant Python should work as well (YMMV).\n\nSQLite3 Update Hook\n-------------------\n\nThe `SQLite3 update\nhook <https://www.sqlite.org/c3ref/update_hook.html>`__ allows the hook\nto be notified if the database to which the connection is made was\nchanged.\n\nThis a drop-in replacement that can be used as demonstrated in the\nexample below. The name ``pysqlite2`` was chosen to the driver to be\ndiscovered automatically by `Django SQLite\nbackend <https://docs.djangoproject.com/en/1.10/ref/databases/#using-newer-versions-of-the-sqlite-db-api-2-0-driver>`__.\n\n.. code:: python\n\n\n    from pysqlite2 import connect\n\n    def hook(conn, op, db_name, table_name, rowid):\n        """Handle notification here. Do not modify the connection!"""\n        \n    with connect(":memory:") as conn:\n        conn.set_update_hook(hook)\n        conn.execute("CREATE TABLE a (int id);")\n        conn.execute("INSERT INTO a VALUES (1);")\n\nYou can also use this library directly with your Python 3 without\nrenaming:\n\n.. code:: python\n\n    from sqlite3 import connect\n    from karellen.sqlite3 import Connection\n\n    with connect(":memory:", factory=Connection):\n        # Do something useful here\n        pass\n\n.. |Gitter chat| image:: https://badges.gitter.im/karellen/gitter.svg\n   :target: https://gitter.im/karellen/lobby\n',
        author = 'Karellen, Inc',
        author_email = 'supervisor@karellen.co',
        license = 'Apache License, Version 2.0',
        url = 'https://github.com/karellen/karellen-sqlite',
        scripts = [],
        packages = [
            'pysqlite2',
            'karellen.sqlite3'
        ],
        namespace_packages = [],
        py_modules = [],
        classifiers = [
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.6',
            'Topic :: Database :: Database Engines/Servers',
            'Topic :: Software Development :: Libraries :: Python Modules'
        ],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = [],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        keywords = '',
        python_requires = '',
        obsoletes = ['pysqlite'],
    )
