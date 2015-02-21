import sys

from setuptools import (
    setup,
    find_packages,
)

python2_install_requires = [
    'py2-ipaddress == 2.0',
]
common_install_requires = [
    'Twisted>=15.0.0, < 16.0.0',
    'Flask == 0.10.1',
    'Flask-Login==0.2.11',
    'python-dateutil >= 2.4.0, < 3.0.0',
]

if sys.version_info >= (3, 0):
    install_requires = common_install_requires
else:
    install_requires = common_install_requires + python2_install_requires

setup(
    name='pyfreelan',
    url='http://pyfreelan.readthedocs.org/en/latest/index.html',
    author='Julien Kauffmann',
    author_email='julien.kauffmann@freelan.org',
    license='GPLv3',
    version=open('VERSION').read().strip(),
    description=(
        "Provides HTTP(S) client/server features to the FreeLAN VPN software"
    ),
    long_description="""\
pyfreelan is the default HTTP(S) client/server integration library for the
FreeLAN VPN software.

It can be used either through the freelan binary, or as a standalone
application.
""",
    packages=find_packages(exclude=[
        'tests',
    ]),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'pyfreelan-server = pyfreelan.main:server_main',
            'pyfreelan-client = pyfreelan.main:client_main',
        ],
    },
    test_suite='tests',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Development Status :: 2 - Pre-Alpha',
    ],
)
