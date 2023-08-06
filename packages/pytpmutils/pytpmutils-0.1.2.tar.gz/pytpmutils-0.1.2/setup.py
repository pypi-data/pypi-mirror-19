import sys

from setuptools import setup
from setuptools import find_packages

version = '0.1.2'

# Please update tox.ini when modifying dependency version requirements
install_requires = [
    'pytss'
]

# env markers in extras_require cause problems with older pip: #517
# Keep in sync with conditional_requirements.py.
if sys.version_info < (2, 7):
    install_requires.extend([
        # only some distros recognize stdlib argparse as already satisfying
        'argparse',
        'mock<1.1.0',
    ])
else:
    install_requires.append('mock')


dev_extras = [
    'nose',
    'pep8',
    'tox',
]

docs_extras = [
    'Sphinx>=1.0',  # autodoc_member_order = 'bysource', autodoc_default_flags
    'sphinx_rtd_theme',
    'sphinxcontrib-programoutput',
]

setup(
    name='pytpmutils',
    version=version,
    description='Basic TPM python utils for Linux',
    url='https://github.com/ph4r05/py-tpm-utils',
    author='Dusan Klinec (ph4r05)',
    author_email='dusan.klinec@gmail.com',
    license=open('LICENSE').read(),
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Security',
    ],

    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    extras_require={
        'dev': dev_extras,
        'docs': docs_extras,
    },

    entry_points={
        'console_scripts': [
            'tpm-rndgen = tpmutils.rnd:main',
            'tpm-rsagen = tpmutils.rsa:main',
        ],
    }
)
