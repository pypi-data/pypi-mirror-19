from setuptools import setup, find_packages
from codecs import open
from os import path
#from whaaaaat import __version__

here = path.abspath(path.dirname(__file__))

# long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# get the dependencies
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if ('git+' not in x) and (
    not x.startswith('#')) and (not x.startswith('-'))]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs \
                    if 'git+' not in x]

setup(
    name='whaaaaat',
    version='0.3.0',
    description=(
          'Collection of common interactive command line user interfaces,'
          ' based on Inquirer.js'
    ),
    long_description=long_description,
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Software Development :: '
        'Libraries :: Application Frameworks',
    ],
    keywords='',
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    author='',
    install_requires=install_requires,
    dependency_links=dependency_links,
    author_email=''
)
