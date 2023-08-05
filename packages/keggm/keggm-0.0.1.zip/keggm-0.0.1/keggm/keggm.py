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
#                                                                              #
# The main parser for keggM    - branches into subparser workflows                  #
#                                                                              #
###############################################################################

from enrichm import enrichm_wf
from completem import completem_wf
from plots import plots_wf
from run_tests import test_wf
from keggscrape import keggscrape_wf

def main(args):
     
    print "The database directory", args.database_dir 
	
    if args.subparser_name=='enrichm':
        dfs=enrichm_wf(args)
    elif args.subparser_name=='completem':
        dfs=completem_wf(args)
    elif args.subparser_name=='plots':
        dfs=plots_wf(args)
    elif args.subparser_name=='tests':
        dfs=tests_wf(args)
    elif args.subparser_name=='keggscrape':
        dfs=keggscrape_wf(args)
        
    return