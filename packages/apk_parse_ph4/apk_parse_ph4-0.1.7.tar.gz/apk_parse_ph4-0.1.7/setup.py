import sys

from setuptools import setup
from setuptools import find_packages

version = '0.1.7'

# Please update tox.ini when modifying dependency version requirements
install_requires = [
    'M2Crypto'
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
    name='apk_parse_ph4',
    version=version,
    description='APK parsing tools',
    url='https://github.com/ph4r05/apk_parse/',
    author='Dusan Klinec (ph4r05)',
    author_email='dusan.klinec@gmail.com',
    maintainer='Dusan Klinec ph4r05',
    maintainer_email='dusan.klinec@gmail.com',
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

    # entry_points={
    #     'console_scripts': [
    #         'tpm-rndgen = tpmutils.rnd:main',
    #     ],
    # }
)
