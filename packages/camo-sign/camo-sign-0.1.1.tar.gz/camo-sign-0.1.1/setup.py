import os
from setuptools import setup, find_packages

version = '0.1.1'

here = os.path.dirname(__file__)

with open(os.path.join(here, 'README.rst')) as fp:
    longdesc = fp.read()

with open(os.path.join(here, 'CHANGELOG.rst')) as fp:
    longdesc += "\n\n" + fp.read()


setup(
    name='camo-sign',
    version=version,
    packages=find_packages(),
    url='https://github.com/bkno3/camo-sign',
    license='BSD License',
    author='Samuele Santi',
    author_email='samuele+gh@samuelesanti.com',
    description='Generate signed URLs for Camo image proxy',
    long_description=longdesc,
    install_requires=[],
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
    ],
    package_data={'': ['README.rst', 'CHANGELOG.rst']},
    include_package_data=True,
    zip_safe=False)
