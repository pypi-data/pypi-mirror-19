from setuptools import setup, find_packages
from codecs import open
from os import path

__version__ = '1.0'

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# get the dependencies and installs
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if 'git+' not in x]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs if x.startswith('git+')]

setup(
    name='s2k',
    version=__version__,
    description='Send files to your Kindle email.',
    long_description=long_description,
    url='https://github.com/hadenpike/s2k',
    download_url='https://github.com/hadenpike/s2k/tarball/' + __version__,
    license='MIT',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Programming Language :: Python :: 3',
    ],
    keywords='',
    packages=find_packages(exclude=['docs']),
    include_package_data=True,
    author='Haden Pike',
    install_requires=install_requires,
    dependency_links=dependency_links,
    author_email='haden.pike@gmail.com',
    entry_points={
        "console_scripts":[
            "s2k=s2k:main",
            ],
        }
)
