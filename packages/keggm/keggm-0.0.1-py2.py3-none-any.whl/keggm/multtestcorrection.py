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
# Multiple test corrections used in keggM                                      #
#                                                                              #
###############################################################################

import statsmodels.sandbox.stats.multicomp as sm

def post_hoc_significance_correction(results_dict,threshold,mult_adjust_type):
    '''Apply the multiple test correction after analysis.'''

    #print results_dict
    #print "THe number of genome pair comparison",results_dict.shape[0]
    print "The number of comparisons made",results_dict.shape[0]
    
    p_vals=results_dict.ix[:,'pvalue']
    #print p_vals
    significant_results=sm.multipletests(p_vals,alpha=threshold,method=mult_adjust_type,returnsorted=False,is_sorted=False)[0]#multiple_test_correction(results_dict,threshold,n,mult_adjust_type)
    
    new_results=results_dict[significant_results]
    
    print "Number of significant results", new_results.shape[0]
    
    return new_results


