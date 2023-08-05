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
#
#
###############################################################################

from enrichment import *
from kegg_core import *
from collections import defaultdict
import pandas as pd

def standard_enrichment_wf(KO_file, groupings_file,comparisons_file,threshold, database_dir, output_dir, bin_file, mult_adjust_type,extras_dict,excluded_set,extra_defs_file,account_for_overlap,make_mo_comps,totals_file):
    '''A workflow for calculating the enrichments of modules in target genomes/groups against other groups as based on 
    the comparisons and groupings file.
    Input:
    
    Output:
    
    '''
    
    bin_taxa=load_bin_taxa(bin_file)
    
    #print bin_taxa

    KO_hits=import_KO_hits(KO_file)
    #print groupings_file
    #print comparisons_file
    if isinstance(groupings_file,type(None)):
        print "No groupings file specified."
        groupings=load_groupings(groupings_file,KO_hits.columns)
        groupings_dict=make_groupings_dict(KO_hits,None,all_grouped=True)
    else:
        groupings=load_groupings(groupings_file,KO_hits.columns)
        groupings_dict=make_groupings_dict(KO_hits,groupings,all_grouped=False)
        
    if isinstance(comparisons_file,type(None)):
        print "No comparisons file specified."
        comparisons_dict=make_comparisons_dict(KO_hits)
        
    else:
        comparisons=load_comparisons(comparisons_file)
        comparisons_dict=comparisons
    
    #Pair up grouping an comparison to get comparison types
    comparisons_dict=identify_tests(comparisons_dict,groupings)
    if isinstance(totals_file,type(None)):
        print "No total counts file specified. Using total number of KOs instead."
        total_counts=None
    else:
        total_counts=load_counts_file(totals_file)
    #for group, KOs in groupings_dict.iteritems():
    #    KO_hits[group]=KOs
    if account_for_overlap:
        overlap_file=construct_overlap_file(comparisons_dict, groupings)
    else:
        overlap_file=None
    #print "This is the overlap for each comparison being made", overlap_file
    if not isinstance(extras_dict,type(None)):
        print "Processing the extras files"
        extras_dict=load_extra_items(extras_dict)
        #print "THe extra items", extras_dict
    if not isinstance(excluded_set,type(None)):
        print "Processing the excluded files"
        excluded_set=load_excluded_items(excluded_set)
    
        
    results_dict=do_enrichment_comparisons(KO_hits,threshold, database_dir, comparisons_dict,extras_dict,excluded_set,extra_defs_file,overlap_file,make_mo_comps,groupings,total_counts)
    
    results_dict=split_results_comparison(results_dict)
    
    results_dict["tested"]=post_hoc_significance_correction(results_dict["tested"],threshold,mult_adjust_type)

    dfs=write_enrichment_data(results_dict, database_dir,output_dir,bin_taxa,mult_adjust_type,extras_dict)
    
    return dfs
    
def enrichm_wf(args):
    
    KO_file=args.KO_file
    groupings_file=args.groupings_file
    comparisons_file=args.comparisons_file
    threshold= args.threshold
    database_dir=args.database_dir
    output_dir=args.output_dir
    bin_file=args.bin_file
    mult_adjust_type=args.mult_test_correction
    excluded_set=args.exclude
    extra_file=args.extra
    extra_defs_file=args.extra_defs
    account_for_overlap=args.remove_overlap
    make_mo_comps=args.make_mo_comps
    totals_file=args.totals_file
    
    dfs=standard_enrichment_wf(KO_file, groupings_file,comparisons_file,threshold, database_dir, output_dir, bin_file, mult_adjust_type,extra_file,excluded_set,extra_defs_file,account_for_overlap,make_mo_comps,totals_file)
    
    return dfs
    
