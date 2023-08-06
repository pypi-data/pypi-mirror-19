import sys
if sys.version_info[0] < 3:
    print("Python version detected:\n*****\n{0!s}\n*****\nCannot run, must be using Python 3".format(sys.version))
    sys.exit()

from setuptools import setup, find_packages
from glob import glob

setup(
    name = 'astrogear',
    packages = find_packages(),
    include_package_data=True,
    version = '0.17.1.11',
    license = 'GNU GPLv3',
    platforms = 'any',
    description = 'Multi-purpose API to build Python applications born in Astronomical context',
    author = 'Julio Trevisan',
    author_email = 'juliotrevisan@gmail.com',
    url = 'https://github.com/trevisanj/astrogear', # use the URL to the github repo
    keywords= ['astronomy', "photometry", "air-to-vacuum", "vacuum-to-air", "rainbow"],
    install_requires = ['numpy', 'scipy', 'matplotlib'],  # Note: matplotlib never gets installed correctly by pip
    scripts = glob('scripts/*.py')  # Considers system scripts all .py files in 'scripts' directory
)

