try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
        'description': 'COSMO auto test',
}

setup(**config)
