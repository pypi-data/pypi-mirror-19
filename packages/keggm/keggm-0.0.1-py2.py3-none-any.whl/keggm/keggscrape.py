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

from kegg_core import *
from mgkit import kegg
import os, sys
import re
import itertools
import pandas as pd

# General Data loading
def store_local_kegg_item_keys(kegg_items,database_dir):
    kc=kegg.KeggClientRest()
    all_item_names={}
    illegal_pairs=[("compound","orthology"),("orthology","compound")]
    for kegg_item in kegg_items:
        key_name=os.path.join(database_dir,"{0}_readable_names.tsv".format(kegg_item))
        if not os.path.isfile(key_name):
            item_names=kc.get_ids_names(kegg_item)
            save_readable_key(key_name,item_names,kegg_item)
            all_item_names[kegg_item]=item_names.keys()
        else:
            all_item_names[kegg_item]=load_readable_names(database_dir,[kegg_item],False)[kegg_item].keys()
    for kegg_item_1, kegg_item_2 in itertools.permutations(all_item_names.iterkeys(),2):
        print "considering the pair: {0}, {1}".format(kegg_item_1,kegg_item_2)
        if (kegg_item_1,kegg_item_2) not in illegal_pairs:
            shared_key_name=os.path.join(database_dir,"{0}_linked_{1}_database.tsv").format(kegg_item_1, kegg_item_2)
            if not os.path.isfile(shared_key_name):
                print "The processing of pair: {0},{1} has begun.".format(kegg_item_1,kegg_item_2)
                kc=kegg.KeggClientRest()
                linked_ids=kc.link_ids(kegg_item_2,all_item_names[kegg_item_1])
                save_key_pairings(shared_key_name,linked_ids,(kegg_item_1,kegg_item_2))
        else:
            pass
    return
    
def make_local_rcn_eqn_database(database_dir):
    kc=kegg.KeggClientRest()
    all_reactions=load_readable_names(database_dir,["reaction"],False)["reaction"].keys()
    rcn_eqns=kc.get_reaction_equations(all_reactions,max_len=10)
    file_name=os.path.join(database_dir, "reaction_equation_links.tsv")
    df=rcn_eqn_pd_df(rcn_eqns)
    df.to_csv(file_name,sep="\t",index=False)
        
    return

def rcn_eqn_pd_df(rcn_eqn_dict):
    df=pd.DataFrame([
            [rcn, ";".join(in_cpds),";".join(out_cpds)] for rcn, cpds in rcn_eqn_dict.iteritems() for in_cpds,out_cpds in [cpds.values()]
    if in_cpds!=[] or out_cpds!=[]    
        ])
    #df.replace('','NA')
    df.columns=["Kegg_rcn_ID","side_1_cpds","side_2_cpds"]
    return df

def make_local_complete_module_info_db(database_dir):
    '''Creates a local database of the module definitions.'''
    all_modules=load_readable_names(database_dir,["module"],False)["module"].keys()
    kc=kegg.KeggClientRest()
    entries={}
    max_len=10
    post_processed_defs={}
    print "There are a total of {0} modules to parse".format(len(all_modules))
    N_modules=len(all_modules)
    for i in xrange(0,N_modules,max_len):
        if N_modules-i<max_len:
            n_entries=N_modules-i
        else:
            n_entries=max_len      
        query="+".join(all_modules[i:i+n_entries])
        kegg_entries=kc.get_entry(query)
        hits=re.findall("\nDEFINITION(.*)\n",kegg_entries)
        print i, i+max_len-1,"n_hits:{0}".format(len(hits))
        #if len(hits)!=max_len:
        #    print m
        for module, definition in itertools.izip(all_modules[i:i+10],hits):
            new_def=definition.strip().replace(" --"," ").replace("-- "," ").replace("  "," ").strip()
            entries[module]=new_def
            if "M" in definition:
                print module,definition
                post_processed_defs[module]=new_def
        #These post_processed modules should be modules defined in terms of other modules.
    for module, definition in post_processed_defs.iteritems():
        new_def=definition
        print "This is the definition being considered.", new_def
        new_defs=re.split("[, +-]",definition)
        for item in new_defs:
            simp_item=item.strip(")").strip("(")
            if simp_item.startswith("M"):
                print "This is the current item",item
                new_def=new_def.replace(simp_item,"("+entries[simp_item]+")")
        print new_def
        entries[module]=new_def
        
    temp_entries=entries
    protein_complexes='(.)?([K][0-9]+[+]){1,}[K][0-9]+(.)?'
    for module, definition in temp_entries.iteritems():
        for match in re.finditer(protein_complexes, definition):
            match_str=match.group()
            if match_str.startswith("(") and match_str.endswith(")"):
                pass
            elif match_str[-1].isdigit() and match_str[0]=="K":
                match_str=match_str[:] #Trim random end characters
                new_match="("+match_str+")"
                entries[module]=entries[module].replace(match_str,new_match)
            elif match_str[0]=="K":
                match_str=match_str[0:-1] #Trim random end characters
                new_match="("+match_str+")"
                entries[module]=entries[module].replace(match_str,new_match)
            elif match_str[-1].isdigit():
                match_str=match_str[1:] #Trim random end characters
                new_match="("+match_str+")"
                entries[module]=entries[module].replace(match_str,new_match)
            else:
                match_str=match_str[1:-1] #Trim random end characters
                new_match="("+match_str+")"
                entries[module]=entries[module].replace(match_str,new_match)
              
        if i%100==0:
            kc=kegg.KeggClientRest()
            print module
    print "{0} modules were parsed".format(len(entries))
    df=pd.DataFrame([
            [module,entry] for module,entry in entries.iteritems()
        ])
    df.columns=["Kegg_id","Kegg_definition"]
    df.to_csv(os.path.join(database_dir,"Module_definitions_pairs_db.tsv"),sep="\t",index=None)
    
    return

def fix_module_orthology_pairs(database_dir):
    '''Replaces the occurences of modules in the module-orthology links to their corresponding KOs'''
    all_pairs=load_local_kegg_database_pairings(database_dir,[["module","orthology"]], False)["module","orthology"]
    new_pairings=[]
    for module,kos in all_pairs.iteritems():
        new_items=[]
        rand_module=False
        for item in kos:
            if item.lower().startswith("m"):
                new_items.extend(all_pairs[item])
                rand_module=True
            else:
                new_items.append(item)
        if rand_module:
            new_pairings.append((module, list(set(new_items))))
    for (module, new_items) in new_pairings:
        all_pairs[module]=new_items
        
    df=pd.DataFrame([
            [col1,";".join(col2)] for col1, col2 in all_pairs.iteritems()
        ])
    df.columns=[kegg_item_tuple[0],kegg_item_tuple[1]]
    fixed_name=os.path.join(database_dir,"")
    df.to_csv(fixed_name,sep="\t",index=None)
    return

    
    
def keggscrape_wf(args):


    return
