from setuptools import (
    setup,
    find_packages,
)

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
    install_requires=[
        'Twisted>=15.0.0, < 16.0.0',
        'Flask == 0.10.1',
        'Flask-Login==0.2.11',
        'py2-ipaddress == 2.0',
    ],
    entry_points={
        'console_scripts': [
            'pyfreelan-server = pyfreelan.main:server_main',
            'pyfreelan-client = pyfreelan.main:client_main',
        ],
    },
    test_suite='tests',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Development Status :: 2 - Pre-Alpha',
    ],
)
