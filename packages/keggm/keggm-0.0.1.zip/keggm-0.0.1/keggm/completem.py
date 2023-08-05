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

from completeness import *
from kegg_core import *
import os, sys

def completem_wf(args):
    #Load in variables
    KO_file=args.KO_file
    #groupings_file=args.groupings_file
    #comparisons_file=args.comparisons_file
    #threshold= args.threshold
    database_dir=args.database_dir
    output_dir=args.output_dir
    bin_file=args.bin_file
    #mult_adjust_type=args.mult_test_correction
    excluded_items=args.exclude
    extra_items=args.extra
    extra_defs=args.extra_defs
    extract_core=args.extract_core
    #process all of the genomes one by one.
    dfs=standard_completeness_wf(KO_file,database_dir,output_dir,bin_file,excluded_items,extra_items,extra_defs,extract_core)
    return dfs

def standard_completeness_wf(KO_file,database_dir,output_dir,bin_file,excluded_set,extras_dict,extra_defs,extract_core):

    bin_taxa=load_bin_taxa(bin_file)
    
    KO_hits=import_KO_hits(KO_file)

    if not isinstance(extras_dict,type(None)):
        print "Processing the extras files"
        extras_dict=load_extra_items(extras_dict)
        #print "THe extra items", extras_dict
    if not isinstance(excluded_set,type(None)):
        print "Processing the excluded files"
        excluded_set=load_excluded_items(excluded_set)
        

    ko_readable_names=readable_kegg_wrapper("orthology",extras_dict,database_dir)
    
    all_modules,hit_KOs=get_module_completeness(KO_hits,database_dir,excluded_set,extras_dict,extra_defs,ko_readable_names)
    
    #print "Number of genomes:", len(all_modules)
    
    #print "The results", all_modules
    readable_names=readable_kegg_wrapper("module",extras_dict,database_dir)
    
    output_file=os.path.join(output_dir, "Genome_module_completeness_matrix.tsv")
    
    output_file_kos=os.path.join(output_dir, "Genome_module_ko_hit_matrix.tsv")
    
    #print "Readable_names:",readable_names
    
    df=write_module_completeness_data(all_modules,output_file,bin_taxa,extract_core,readable_names)
    
    KO_module_hits=write_module_ko_data(hit_KOs,output_file_kos,bin_taxa,readable_names)
    
    return df,KO_module_hits