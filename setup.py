from setuptools import setup, find_packages

extra_requirements = {
    'testing': [
        # Used to provide testing help
        'pycommon-test==4.9.0',
    ],
    # Used to manage authentication
    'authentication': [
        'oauth2helper==1.4.0',
    ],
    # Used to connect to a Microsoft Windows computer
    'windows': [
        'pysmb==1.1.27',
    ],
    # Async task execution using celery
    'celery': [
        'redis==2.10.6',  # Stick to this version until we upgrade our redis version running on Azure
        # Used to process requests asynchronously
        'celery[redis]==4.2.1',
    ],
    # Used to connect to another REST API
    'rest': [
        'requests==2.21.0',
    ],
}

# Add all extra requirements to testing
extra_requirements['testing'] += [
    extra
    for extra_name, extra_list in extra_requirements.items()
    if extra_name != 'testing'
    for extra in extra_list
]


from pycommon_server._version import __version__

setup(
    name='pycommon_server',
    version=__version__,
    packages=find_packages(exclude=[
        'test',
    ]),
    install_requires=[
        # Used to manage endpoints and swagger
        'flask-restplus==0.12.1',
        # Used to parse configurations
        'PyYAML==3.13',
        # Cross Origin handling
        'flask_cors==3.0.7',
        # Used to gz compress http output
        'flask_compress==1.4.0',
    ],
    extras_require=extra_requirements,
)