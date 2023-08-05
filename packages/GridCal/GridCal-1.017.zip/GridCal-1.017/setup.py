from distutils.core import setup
import sys
import os

name = "GridCal"

# Python 2.4 or later needed
if sys.version_info < (2, 4, 0, 'final', 0):
    raise (SystemExit, 'Python 2.4 or later is required!')

# Build a list of all project modules
packages = []
for dirname, dirnames, filenames in os.walk(name):
        if '__init__.py' in filenames:
            packages.append(dirname.replace('/', '.'))

package_dir = {name: name}



setup(
    # Application name:
    name=name,

    # Version number (initial):
    version="1.017",

    # Application author details:
    author="Santiago Peñate Vera",
    author_email="santiago.penate.vera@gmail.com",

    # Packages
    packages=packages,

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="http://pypi.python.org/pypi/GridCal/",

    #
    # license="LICENSE.txt",
    description="Research Oriented electrical simulation software.",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=["numpy",
                      "scipy",
                      "networkx",
                      "pandas",
                      "PyQt5",
                      "matplotlib",
                      "qtconsole"
                      ],
)