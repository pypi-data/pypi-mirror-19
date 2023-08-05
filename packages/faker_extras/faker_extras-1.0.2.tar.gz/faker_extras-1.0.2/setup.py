"""Installation setup."""

try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()

PACKAGE = 'faker_extras'
VERSION = '1.0.2'

keywords = ['faker_extras', 'fake data generation', 'faker', 'data generator']
description = ('An extended set of data providers for the Faker library.')
setup(
    name='faker_extras',
    version=VERSION,
    description=description,
    author='Chris Tabor',
    author_email='dxdstudio@gmail.com',
    maintainer='Chris Tabor',
    maintainer_email='dxdstudio@gmail.com',
    url='https://github.com/christabor/faker_extras',
    keywords=keywords,
    license='Apache License 2.0',
    package_dir={'faker_extras': 'faker_extras'},
    packages=['faker_extras'],
    zip_safe=False,
    install_requires=[
        'Faker',
    ],
    setup_requires=[
        'setuptools>=0.8',
    ],
    tests_require=[
        'pytest',
    ],
    test_suite='tests',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
    ]
)
