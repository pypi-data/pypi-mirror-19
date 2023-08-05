from setuptools import setup, find_packages

setup(
    name = 'lightcurve',
    url = 'http://justincely.github.io/lightcurve/',
    version = '0.6.0',
    description = 'Create lightcurves from HST/COS and HST/STIS data',
    author = 'Justin Ely',
    author_email = 'ely@stsci.edu',
    keywords = ['astronomy'],
    classifiers = ['Programming Language :: Python',
                   'Programming Language :: Python :: 3',
                   'Development Status :: 1 - Planning',
                   'Intended Audience :: Science/Research',
                   'Topic :: Scientific/Engineering :: Astronomy',
                   'Topic :: Scientific/Engineering :: Physics',
                   'Topic :: Software Development :: Libraries :: Python Modules'],
    packages = find_packages(),
    install_requires = ['astropy',
                        'numpy>=1.9',
                        'scipy',
                        'numba>=0.24.0',
                        'llvmlite>=0.9.0',
                        'nose',
                        'six',
                        'sphinx-automodapi'],
    scripts =  ['scripts/lightcurve'],
    )
