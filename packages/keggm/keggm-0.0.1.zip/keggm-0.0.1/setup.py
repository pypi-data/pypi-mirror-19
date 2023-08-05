#!/usr/bin/env python
###############################################################################
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program. If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################

from setuptools import find_packages, setup

setup(name="keggm",
      version="0.0.1",
      description="A tool for doing enrichment tests of functional groupings of genes across genomes and lineages.",
      author="Alexander Robert Baker",
      author_email='alexander.baker@uqconnect.edu.au',
      platforms=["any"],
      license="GNU GPL3+",
      url="http://github.com/AlexRBaker/",
      packages=find_packages(),
	  keywords="kegg",
	  scripts=['bin/keggm'],
	  install_requires=('pandas>=0.17.1',
	  	'numpy>=1.0.1',
	  	'seaborn>=0.7.1',
	  	'scipy>=0.16.1')
     )