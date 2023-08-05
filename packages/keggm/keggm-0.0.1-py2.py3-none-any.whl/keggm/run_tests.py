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

from kegg_core import *
import enrichm
import completem
import plots
import keggscrape

def test_wf(args):
    
    
    return
    
def test_all_local_modules(database_dir):
    #758 comparisons are to be made.
    completeness_dict={}
    #Load all possible KOs
    MO_KO_pairs=load_local_kegg_database_pairings(database_dir,[("Module","orthology")], False)[("Module","orthology")]
    MO_KO_pairs={MO:set(KOs) for MO, KOs in MO_KO_pairs.iteritems()}
    #Use this as the comparison set.
    log_kegg_exprs=load_local_cleaned_definition_db(database_dir)
    #Screen every single module for compelteness (should all be 1.0)
    for module,expression in log_kegg_exprs.iteritems():
        completeness_dict[module]=module_completeness_proportion(expression,MO_KO_pairs[module],True)
        
    
    failures={Module:completeness for Module,completeness in completeness_dict.iteritems() if completeness<1}
    print failures
    
    return completeness_dict

