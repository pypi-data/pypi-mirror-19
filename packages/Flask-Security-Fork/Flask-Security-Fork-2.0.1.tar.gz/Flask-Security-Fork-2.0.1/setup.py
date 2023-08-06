# -*- coding: utf-8 -*-

"""Simple security for Flask apps."""

from setuptools import find_packages, setup

readme = open('README.rst').read()

tests_require = [
    'Flask-CLI>=0.4.0',
    'Flask-Mongoengine>=0.7.0',
    'Flask-Peewee>=0.6.5',
    'Flask-SQLAlchemy>=1.0',
    'bcrypt>=1.0.2',
    'check-manifest>=0.25',
    'coverage>=4.0',
    'isort>=4.2.2',
    'mock>=1.3.0',
    'mongoengine>=0.10.0',
    'pydocstyle>=1.0.0',
    'pytest-cache>=1.0',
    'pytest-cov>=2.4.0',
    'pytest-flakes>=1.0.1',
    'pytest-pep8>=1.0.6',
    'pytest>=3.0.5',
]

extras_require = {
    'docs': [
        'Flask-Sphinx-Themes>=1.0.1',
        'Sphinx>=1.4.2',
    ],
    'tests': tests_require,
}

extras_require['all'] = []
for reqs in extras_require.values():
    extras_require['all'].extend(reqs)

setup_requires = [
    'pytest-runner>=2.6.2',
]

install_requires = [
    'Flask>=0.10',
    'Flask-Login>=0.3.0',
    'Flask-Mail>=0.7.3',
    'Flask-Principal>=0.3.3',
    'Flask-WTF>=0.13.1',
    'itsdangerous>=0.21',
    'passlib>=1.6.4',
]

packages = find_packages()

setup(
    name='Flask-Security-Fork',
    version='2.0.1',
    description=__doc__,
    long_description=readme,
    keywords='flask security',
    license='MIT',
    author='Matt Wright',
    author_email='matt@nobien.net',
    url='https://github.com/inveniosoftware/flask-security-fork',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Development Status :: 4 - Beta',
    ],
)
