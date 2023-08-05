# This Python file uses the following encoding: utf-8


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    import os
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

from setuptools import setup, find_packages

package_name='netcdf4_pydap'
setup(
       name = package_name,
       version = "0.2.5",
       packages = find_packages(),
#
#        # metadata for upload to PyPI
        author = "F. B. Laliberte",
        author_email = "laliberte.frederic@gmail.com",
        description = "netCDF4 and CAS compatibility layer for pydap",
        license = "MIT",
        keywords = "atmosphere climate",
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Science/Research",
            "Natural Language :: English",
            "License :: OSI Approved :: BSD License",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Fortran"
        ],
        long_description=read('README.rst'),
        install_requires = [
                            'requests>=1.1.0',
                            'requests_cache',
                            'netCDF4',
                            'pydap==3.1.1',
                            'MechanicalSoup'],
        zip_safe=False,
    )
