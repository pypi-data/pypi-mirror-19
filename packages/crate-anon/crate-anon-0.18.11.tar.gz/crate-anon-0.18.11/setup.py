#!/usr/bin/env python
# setup.py

"""
CRATE setup file

To use:

    python setup.py sdist

    twine upload dist/*

To install in development mode:

    pip install -e .

"""
# https://packaging.python.org/en/latest/distributing/#working-in-development-mode  # noqa
# http://python-packaging-user-guide.readthedocs.org/en/latest/distributing/
# http://jtushman.github.io/blog/2013/06/17/sharing-code-across-applications-with-python/  # noqa

from setuptools import setup, find_packages
from codecs import open
# import fnmatch
import os
import platform

from crate_anon.version import VERSION

here = os.path.abspath(os.path.dirname(__file__))

# setup.py is executed on the destination system at install time, so:
windows = platform.system() == 'Windows'

# -----------------------------------------------------------------------------
# Get the long description from the README file
# -----------------------------------------------------------------------------
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# -----------------------------------------------------------------------------
# Get all filenames
# -----------------------------------------------------------------------------
# rootdir = os.path.join(here, 'crate')
# data_files = []
# for dir_, subdirs, filenames in os.walk(rootdir):
#     files = []
#     reldir = os.path.relpath(dir_, rootdir)
#     for pattern in ['*.py', '*.html']:
#         for filename in fnmatch.filter(filenames, pattern):
#             files.append(filename)
#     if files:
#         data_files.append((reldir, files))
# print(data_files)
# http://stackoverflow.com/questions/2186525/use-a-glob-to-find-files-recursively-in-python  # noqa
# http://stackoverflow.com/questions/27664504/how-to-add-package-data-recursively-in-python-setup-py  # noqa

# rootdir = os.path.join(here, 'crate', 'crateweb', 'static_collected')
# static_collected = []
# for dir_, subdirs, filenames in os.walk(rootdir):
#     reldir = os.path.normpath(os.path.join(
#         'static_collected', os.path.relpath(dir_, rootdir)))
#     for filename in filenames:
#         if filename in ['.gitignore']:
#             continue
#         static_collected.append(os.path.join(reldir, filename))

# -----------------------------------------------------------------------------
# setup args
# -----------------------------------------------------------------------------
setup(
    name='crate-anon',  # 'crate' is taken

    version=VERSION,

    description='CRATE: clinical records anonymisation and text extraction',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/RudolfCardinal/crate',

    # Author details
    author='Rudolf Cardinal',
    author_email='rudolf@pobox.com',

    # Choose your license
    license='GNU General Public License v3 or later (GPLv3+)',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',  # noqa

        'Natural Language :: English',

        'Operating System :: OS Independent',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3 :: Only',

        'Topic :: System :: Hardware',
        'Topic :: System :: Networking',
    ],

    keywords='anonymisation',

    packages=find_packages(),  # finds all the .py files in subdirectories
    package_data={
        '': [
            'README.md'
        ],
        'crate_anon.crateweb': [
            # Don't use 'static/*', or at the point of installation it gets
            # upset about "demo_logo" ("can't copy... doesn't exist or not
            # a regular file). Keep running "python setup.py sdist >/dev/null"
            # until stderr comes up clean.
            'consent/templates/*.html',
            'consent/templates/*.js',
            'research/templates/*.html',
            'static/*.gif',
            'static/*.ico',
            'static/*.png',
            'static/demo_logo/*',
            'templates/*.css',
            'templates/*.html',
            'templates/*.js',
            'templates/admin/*.html',
            'userprofile/templates/*.html',
        ],
        'crate_anon.nlp_manager': [
            '*.java',
            '*.sh',
        ],
        'crate_anon.mysql_auditor': [
            '*.conf',
            '*.lua',
            '*.sh',
        ],
    },

    install_requires=[

        # ---------------------------------------------------------------------
        # For the web front end:
        # ---------------------------------------------------------------------
        # Core tools with accessories:
        'arrow==0.7.0',  # better datetime
        'colorlog==2.6.1',  # colour in logs
        # 'configobj==5.0.6',  # better config files
        'distro==0.6.0',  # replaces platform.linux_distribution
        # requires VC++ under Windows # 'mmh3==2.2',  # MurmurHash, for fast non-cryptographic hashing  # noqa
        'psutil==4.1.0',  # process management
        'pyhashxx==0.1.3',  # fast non-cryptographic hashing
        'semver==2.4.1',  # comparing semantic versions
        'SQLAlchemy>=1.1.3',  # database access
        'typing==3.5.2.2',  # part of stdlib in Python 3.5, but not 3.4

        # Web app:
        'celery==3.1.23',
        'colorlog==2.6.1',
        'Django>=1.9.3',  # "django" versus "Django": neither helps pycharm checking  # noqa
        'django-debug-toolbar==1.4',
        'django-debug-toolbar-template-profiler==1.0.1',
        'django-extensions==1.5.9',
        'django-picklefield==0.3.2',
        # 'django-silk==0.5.7',
        'django-sslserver==0.15',
        'flower==0.9.1',  # debug Celery; web server; only runs explicitly
        'pdfkit==0.5.0',
        # 'pygraphviz==1.3.1',  # not used
        'pyparsing==2.1.5',  # generic grammar parser
        'PyPDF2==1.25.1',
        'pytz==2015.6',
        'python-dateutil==2.4.2',
        'sqlparse==0.1.19',
        'Werkzeug==0.10.4',

        # ONSPD:
        'openpyxl==2.3.5',
        'xlrd==1.0.0',

        # Serving:
        'gunicorn==19.3.0',  # UNIX only, though will install under Windows
        'cherrypy==5.1.0',  # Cross-platform

        # ---------------------------------------------------------------------
        # For the anonymiser/pythonlib:
        # ---------------------------------------------------------------------

        'cardinal_pythonlib==0.2.4',

        'beautifulsoup4==4.4.1',
        'prettytable==0.7.2',
        # 'python-docx==0.8.5',  # needs lxml, which has Visual C++ dependencies under Windows  # noqa
        # ... https://python-docx.readthedocs.org/en/latest/user/install.html
        'regex==2015.11.14',
        'sortedcontainers==1.4.2',

        # ---------------------------------------------------------------------
        # For database connections (see manual): install manually
        # ---------------------------------------------------------------------
        # MySQL: one of:
        #   'PyMySQL',
        #   'mysqlclient',
        # SQL Server / ODBC route:
        #   'django-pyodbc-azure',
        #   'pyodbc',  # has C prerequisites
        #   'pypyodbc==1.3.3',
        # SQL Server / Embedded FreeTDS route:
        #   'django-pymssql',
        #   'django-mssql',
        #   'pymssql',
        # PostgreSQL:
        #   'psycopg2',  # has prerequisites (e.g. pg_config executable)
    ] + ([
        'pypiwin32==219'
    ] if windows else []),

    entry_points={
        'console_scripts': [
            # Format is 'script=module:function".
            'crate_make_demo_database=crate_anon.anonymise.make_demo_database:main',  # noqa
            'crate_anonymise=crate_anon.anonymise.anonymise_cli:main',
            'crate_anonymise_multiprocess=crate_anon.anonymise.launch_multiprocess_anonymiser:main',  # noqa
            'crate_test_anonymisation=crate_anon.anonymise.test_anonymisation:main',  # noqa
            'crate_test_extract_text=crate_anon.anonymise.test_extract_text:main',  # noqa
            'crate_nlp=crate_anon.nlp_manager.nlp_manager:main',
            'crate_nlp_multiprocess=crate_anon.nlp_manager.launch_multiprocess_nlp:main',  # noqa
            'crate_nlp_build_gate_java_interface=crate_anon.nlp_manager.build_gate_java_interface:main',  # noqa
            'crate_nlp_build_medex_java_interface=crate_anon.nlp_manager.build_medex_java_interface:main',  # noqa
            'crate_nlp_build_medex_itself=crate_anon.nlp_manager.build_medex_itself:main',  # noqa

            'crate_generate_new_django_secret_key=crate_anon.tools.generate_new_django_secret_key:main',  # noqa
            'crate_estimate_mysql_memory_usage=crate_anon.tools.estimate_mysql_memory_usage:main',  # noqa

            'crate_django_manage=crate_anon.crateweb.manage:main',  # will cope with argv  # noqa
            'crate_launch_django_server=crate_anon.crateweb.manage:runserver',
            'crate_launch_cherrypy_server=crate_anon.tools.launch_cherrypy_server:main',  # noqa
            # ... a separate script with ":main" rather than
            # "crate_anon.crateweb.manage:runcpserver" so that we can launch
            # the "runcpserver" function from our Windows service, and have it
            # deal with the CherryPy special environment variable
            'crate_launch_celery=crate_anon.tools.launch_celery:main',
            'crate_launch_flower=crate_anon.tools.launch_flower:main',
            'crate_print_demo_crateweb_config=crate_anon.tools.print_crateweb_demo_config:main',  # noqa

            'crate_windows_service=crate_anon.tools.winservice:main',

            'crate_postcodes=crate_anon.preprocess.postcodes:main',
            'crate_preprocess_rio=crate_anon.preprocess.preprocess_rio:main',
        ],
    },
)
