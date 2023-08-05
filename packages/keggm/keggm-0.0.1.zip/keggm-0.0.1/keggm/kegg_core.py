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
# core - contains functions used in many different workflows                  # 
#                                                                              #
###############################################################################

import os, sys
from collections import Counter
from collections import defaultdict
from glob import glob
import re
import itertools
import pandas as pd
from completeness import *

def all_hits(row):
    return all(row>0)

def any_hits(row):
    return any(row>0)

def make_sets_from_df(df):
    ko_set={}
    for genome, KOs in df.iteritems():
        ko_set[genome]=make_KO_set_from_series(KOs)
    
    return ko_set
    
def load_local_kegg_database_pairings(database_dir,kegg_item_pairs, process_all):
    '''Loads the local databases of kegg_item_1, kegg_item_2 pairings and return a dictionary of
    these pairings in the form kegg_item_1:kegg_items_2 (There can be more than one linked item). This
    loading is based on the earlier use of mgkits kc.link_ids to store all of the pairings needed.
    
    Input:
        database_dir   - The directory with the databases
        kegg_item_pairs- A list of kegg item pairs to load
        process_all    - A boolean decision as whether to load all existing pairs.
        
    Output: A dictionary linking either all existing kegg item pairs or just those specified. It has the form
    dict[item_1,item_2]={kegg_item_1:kegg_2_items}'''
    linking_dictionary={}
    if process_all:
        for file_name in glob(os.path.join(database_dir,'*database.tsv')):
            db_file=os.basename(file_name)
            kegg_1=db_file.split("_linked_")[0]
            kegg_2=db_file.split("_linked_")[1].split("_database")[0]
            linking_dictionary[(kegg_1,kegg_2)]={}             
            with open(file_name) as kegg_links:
                next(kegg_links)#Skip the header
                for line in kegg_links:
                    item_1,item_2=line.strip().split("\t")
                    item_2=item_2.split(";")
                    linking_dictionary[kegg_item_pair][item_1]=item_2
        return linking_dictionary
    
    for kegg_item_pair in kegg_item_pairs:
        file_name=os.path.join(database_dir,"{0}_linked_{1}_database.tsv").format(kegg_item_pair[0], kegg_item_pair[1])
        if os.path.isfile(file_name):
            linking_dictionary[kegg_item_pair]={}
            with open(file_name) as kegg_links:
                next(kegg_links) #skip the header
                for line in kegg_links:
                    item_1,item_2=line.strip().split("\t")
                    item_2=item_2.split(";")
                    linking_dictionary[kegg_item_pair][item_1]=item_2
    return linking_dictionary
                    
def load_readable_names(database_dir,kegg_items,process_all):
    '''Loads in the readable names for a specified kegg item from a list of databases.
    Input:
        database_dir        -  The directory with the databases.
        kegg_items          -  The kegg items to get the readable mapping for.
        process_all         -  Boolean - Should the function retrieve all available databases.
    Output:
        readable_item_dict  -  A dictionary of KEGG_ID: Readable name pairs'''
    readable_item_dict={}
    if process_all:
        for file_name in glob(os.path.join(database_dir,'*_readable_names.tsv')):
            desc_file=os.basename(file_name)
            kegg_item=desv_file.split("_readable_names.tsv")[0]
            readable_item_dict[kegg_item]={}
            with open(file_name) as kegg_descriptions:
                next(kegg_descriptions)
                for line in kegg_descriptions:
                    item_1,item_2=line.strip().split("\t")
                    readable_item_dict[kegg_item][item_1]=item_2
        return readable_item_dict
    
    for kegg_item in kegg_items:
        file_name=os.path.join(database_dir,'{0}_readable_names.tsv'.format(kegg_item))
        readable_item_dict[kegg_item]={}
        with open(file_name) as kegg_descriptions:
            next(kegg_descriptions)
            for line in kegg_descriptions:
                item_1,item_2=line.strip().split("\t")
                readable_item_dict[kegg_item][item_1]=item_2
    return readable_item_dict
    
def save_readable_key(key_name,item_names,kegg_item):
    df=pd.DataFrame([
    [col1,col2] for col1,col2 in item_names.iteritems()
                   ])
    df.columns=[kegg_item,"Description"]
    df.to_csv(key_name,sep="\t",index=None)
    return None

def save_key_pairings(shared_key_name,item_links,kegg_item_tuple):
    df=pd.DataFrame([
            [col1,";".join(col2)] for col1, col2 in item_links.iteritems()
        ])
    df.columns=[kegg_item_tuple[0],kegg_item_tuple[1]]
    df.to_csv(shared_key_name,sep="\t",index=None)
    return None
    
def load_local_rcn_eqn_database(database_dir):
    file_name=os.path.join(database_dir,"reaction_equation_links.tsv")
    rcn_eqn_dict={}
    n_df=pd.read_csv(file_name,sep="\t")
    n_df.fillna('',inplace=True)
    return n_df.set_index("Kegg_rcn_ID").T.to_dict(orient='dict')
    
#Load in the coral data
def load_bin_names(tax_file):
    #Load bin_ids and bins_taxonomy from file.
    bin_names={}
    bin_pair=[]
    with open(tax_file,'r') as bin_tax_pair:
        bin_tax_pair.readline()
        for line in bin_tax_pair:
            bin_pair.append(tuple(line.strip().split("\t")))

    bin_names={bin_id:taxonomy for taxonomy, bin_id in bin_pair}
    return bin_names
    
def make_new_trusted_database(database_dir):
    '''
    Definition:
        This function will take an entire kegg module definition file and will create
        a new local database with the expressions written so that they can simple be
        evaluated when loading the files.
    Input: 
        database_dir: str
            A directory containing the database of kegg module definitions.
    Output:
        None
    Calls:
        replacement: Turns kegg definitions in logical nested tuples of sets.
    '''
    old_module_def=load_local_complete_module_info_db(database_dir)
    #print "This is the old module information",old_module_def
    new_pd_df=[""]*len(old_module_def)
    i=0
    for module,definition in old_module_def.iteritems():
        try:
            logical_evaluation=replacement(definition,False)[1]
            new_pd_df[i]=[module,logical_evaluation]
            i+=1
                
        except TypeError:
            print "TypeError 2:",module, definition
        except SyntaxError:
            print "SyntaxError 2:",module, definition
        except NameError:
            print "NameError 2:",module ,definition
    #print new_pd_df      
    new_pd_df=pd.DataFrame(new_pd_df)
    #print "The second checkpoint."
    new_pd_df.columns=["ModuleID","KEGG_log_expr"]
    
    new_pd_df.to_csv(os.path.join(database_dir, "module_kegg_log_expr.tsv"),header=True,sep="\t",index=False)
    return None
    
def load_local_rcn_eqn_database_set(database_dir):
    rcn_eqn_pairs=load_local_rcn_eqn_database(database_dir)
    return {rcn:{side:set(cpds.split(";")) for side,cpds in pairs.iteritems()} for rcn, pairs in rcn_eqn_pairs.iteritems()}
            
def load_local_complete_module_info_db(database_dir):
    '''Loads a local database of kegg definitions'''
    def_dict={}
    with open(os.path.join(database_dir,"Module_definitions_pairs_db.tsv")) as definitions:
        next(definitions)
        for line in definitions:
            module,kegg_def=line.strip().split("\t")
            def_dict[module]=kegg_def
    
    return def_dict
    
def load_local_cleaned_definition_db(extra_def_file):
    cleaned_db={}
    with open(os.path.join(extra_def_file)) as paired_exprs:
        next(paired_exprs) #Skip header
        for line in paired_exprs:
            module,expr=line.split("\t")
            kegg_log=eval(expr)
            if not isinstance(kegg_log,tuple):
                kegg_log=tuple([kegg_log])
            cleaned_db[module]=kegg_log
    return cleaned_db
    
def import_KO_hits(file_name):  
    #Needs to detect counts file and rewrite it.
    KO_hits={}
    with open(file_name) as KO_hits_file:
        header_line=next(KO_hits_file)
        if len(header_line.split("\t"))>2:
            dataframe=True
        else:
            dataframe=False
    if not dataframe:
        with open(file_name) as KO_hits_file:
            for line in KO_hits_file:
                genome,KOs=line.strip().split("\t")
                KOs=KOs.split(";")
                #print genome,KOs
                KO_hits[genome]=KOs
        #print "THE KO HITS", KO_hits
        KO_hits_dup=KO_hits
        for genome, KOs in KO_hits.iteritems():
            KO_hits[genome]=Counter(KOs)
        KO_hits=pd.DataFrame.from_dict(KO_hits,orient='columns')
        KO_hits=KO_hits.fillna(0)
        #print "THe Ko hits", KO_hits
        return KO_hits
    elif dataframe:
        KO_hits=convert_kegg_hits_to_occurrences(file_name)
        #print "THE KO HITS", KO_hits
        return KO_hits
    else:
        print "Error"
        return

def convert_kegg_hits_to_occurrences(file_name):
    counts_df=pd.read_csv(file_name,sep="\t",index_col=[0])
    #KO_dict={}
    #for genome in counts_df.columns:
    #    KO_dict[genome]=[]#*n_kos

    #for index,row in counts_df.iterrows():
    #    for genome, count in row.iteritems():
    #        #print index, count
    #        KO_dict[genome].extend((index,)*count)
    #
    counts_df=counts_df.fillna(0)
    return counts_df

def load_groupings(file_name,all_members):
    '''Loads in a tab separated files of the form: group_name\tgenome_1|genome_2|genome_3|genome_4|etc
    Input:
        file_name: str
            Name of groupings file
    Output:
        groupings: dict
            Dictionary of group name and the list of component genomes'''
    groupings={}
    if not isinstance(file_name,type(None)):
        if not os.path.isfile(file_name):
            raise IOError('The specified groupings file does not exist.')

        with open(file_name) as groupings_file:

            next(groupings_file) #skip header

            for line in groupings_file:
                group_name,members=line.strip().split("\t")
                list_of_members=members.split("|")

                groupings[group_name]=list_of_members
    else:
        groupings["all_genomes_grouped"]=list(all_members)
    #print 'The groupings', groupings   
    return groupings

def load_comparisons(file_name):
    '''Loads in a tab separated files of the form: source_group\ttarget_1|target_2|target_3|etc
    
    Input:
        file_name: str
            Name of comparisons file
    Output:
        comparisons: dict
            Dictionary of baseline gorup name and the list of target group/genome_names to look
            for enrichment in'''
    comparisons={}
    if not os.path.isfile(file_name):
        raise IOError('The specified comparisons file does not exist.')
    with open(file_name) as comparisons_file:
        
        next(comparisons_file) #skip header
        
        for line in comparisons_file:
            source,targets=line.strip().split("\t")
            list_of_targets=targets.split("|")
            comparisons[source]=list_of_targets
    #print 'The comparisons', comparisons
    return comparisons

def make_comparisons_dict(KO_hits):
    '''Makes a default comparison of each individual against the grouping of all.
    Input: 
        KO_hits: dict
            dictionary of all KO_hits for each genome
    returns:
        comparison_dict: dict
            Dictionary with one key (all_genomes_grouped:list of genomes)'''
    return {"all_genomes_grouped":KO_hits.keys()}

def make_groupings_dict(KO_hits,groups, all_grouped=False):
    '''Make a list of KOs for each group based on the KOs of group members.
    Input:
    
    Output:
    '''
    group_KOs={}
    if all_grouped:
        KO_hits["all_genomes_grouped"]=KO_hits.sum(axis=1)
        #group_KOs["all_genomes_grouped"]=list(itertools.chain(*KO_hits.itervalues()))
        print "KO_HITS",KO_hits
        return KO_hits
    else:
        for group, members in groups.iteritems():
            KO_hits[group]=KO_hits.loc[:,members].sum(axis=1)
            #group_KOs[group]=list(itertools.chain(*[KO_hits[member] for member in members]))
        #print "KO_HITS",KO_hits
        return KO_hits
        
def load_bin_taxa(bin_file):
    bin_names={}
    
    with open(bin_file) as taxonomy:
        next(taxonomy) #skip header
        for line in taxonomy:
            
            taxa,ID=line.strip().split("\t")
            bin_names[ID]=taxa
            
    bin_taxa=defaultdict(lambda:"No_Associated_Taxonomy" ,bin_names)
    
    return bin_taxa

def load_excluded_items(excluded_file):
    excluded_items=[]
    with open(excluded_file) as ignored:
        for line in ignored:
            excluded_items.append(line.strip())
    return set(excluded_items)

def load_extra_items(extras_file):
    extra_items={}
    with open(extras_file) as extras:
        for line in extras:
            ID, KOs=line.strip().split("\t")
            extra_items[ID]=KOs.split(";")
    return extra_items

def make_extras_logical(extra_def_file,extras_dict,database_dir):
    definition_dict={}
    if extra_def_file==None:
        rename_logical=os.path.join(database_dir,"module_extra_kegg_log_expr.tsv")
        for key,KOs in extras_dict.iteritems():
            n_KOs=len(KOs)
            new_def=[' ']*(2*n_KOs-1)
            for i,KO in enumerate(KOs):
                new_def[2*i]=set([KO])
                #if i==(n_KOs-1):
                    #pass
                #else:
                    #new_def[2*i+1]=' '
            definition_dict[key]=tuple(new_def)
        pd_df=pd.DataFrame([
                [module,definition] for module, definition in definition_dict.iteritems()
            ])
        pd_df.columns=["Module","KEGG_Boolean"]
        pd_df.to_csv(rename_logical,header=True,sep="\t",index=False)
        extra_def_file=rename_logical
        
    else:
        pd_df=[]
        core,file_ending=os.path.splitext(extra_def_file)
        rename_logical=core+"KEGG_bool"+file_ending
        with open(extra_def_file) as kegg_defs:
            for line in kegg_defs:
                module, definition=line.strip().split()
                new_def=replacement(definition)
                pd_df.append([module,new_def])
        pd_df=pd.DataFrame(pd_df)
        pd_df.columns=["Module_Name","Logical_definition"]
        pd_df.to_csv(rename_logical,header=True,sep="\t")
        extra_def_file=rename_logical
        
    return extra_def_file

   
    
def kegg_pairs_wrapper(kegg_items,excluded_items, extra_items,database_dir):
    '''
    ********************************************************************************************************
    This function acts as a wrapper to load in the local pairs databases.
    It also excludes those items mentioned in the excluded items list and adds the user defined extra items.
    ********************************************************************************************************
    Input:
    
    Output:
    
    Calls:
    
    '''
    #print "THese are the excluded items", excluded_items
    kegg_item_1,kegg_item_2=kegg_items
    if kegg_item_1=="orthology":
        if isinstance(extra_items,type(None)):
            KO_KG_ITEM_PAIRS=load_local_kegg_database_pairings(database_dir,[("orthology",kegg_item_2)], False)[("orthology",kegg_item_2)]
            if excluded_items!=None:
                #valid_PAIRS=set(KO_KG_ITEM_PAIRS.keys())-set(excluded_items)
                #print "These are the excluded items", excluded_items
                KO_KG_ITEM_PAIRS={key:set(value)-set(excluded_items) for key,value in KO_KG_ITEM_PAIRS.iteritems()}
            #KO_KG_ITEM_PAIRS=add_extra_items_values(KO_KG_ITEM_PAIRS,extra_items)
        else:
            #print "The extra items",extra_items
            KO_KG_ITEM_PAIRS=load_local_kegg_database_pairings(database_dir,[("orthology",kegg_item_2)], False)[("orthology",kegg_item_2)]
            if excluded_items!=None:
                #valid_PAIRS=set(KO_KG_ITEM_PAIRS.keys())-set(excluded_items)
                #print "These are the excluded items", excluded_items
                KO_KG_ITEM_PAIRS={key:set(value)-set(excluded_items) for key,value in KO_KG_ITEM_PAIRS.iteritems()}
            KO_KG_ITEM_PAIRS=add_extra_items_values(KO_KG_ITEM_PAIRS,extra_items)
        return KO_KG_ITEM_PAIRS
    
    elif kegg_item_2=="orthology":
        if isinstance(extra_items,type(None)):
            KG_ITEM_KO_PAIRS=load_local_kegg_database_pairings(database_dir,[(kegg_item_1,"orthology")], False)[(kegg_item_1,"orthology")]
            if excluded_items!=None:
                valid_PAIRS=set(KG_ITEM_KO_PAIRS.keys())-set(excluded_items)
                KG_ITEM_KO_PAIRS={key:value for key,value in KG_ITEM_KO_PAIRS.iteritems() if key in valid_PAIRS}
        else:
            KG_ITEM_KO_PAIRS=load_local_kegg_database_pairings(database_dir,[(kegg_item_1,"orthology")], False)[(kegg_item_1,"orthology")]
            if excluded_items!=None:
                valid_PAIRS=set(KG_ITEM_KO_PAIRS.keys())-set(excluded_items)
                KG_ITEM_KO_PAIRS={key:value for key,value in KG_ITEM_KO_PAIRS.iteritems() if key in valid_PAIRS}
            for name, KOs in extra_items.iteritems():
                KG_ITEM_KO_PAIRS[name]=KOs
            
        return KG_ITEM_KO_PAIRS
    else:
        print "The input kegg item pair must have at least one occurence of orthology."
        
    return

def add_extra_items_values(dict_1, extra_items_dict):
    ''' Swaps the keys and values of the dictionary. Then, add these to the orthology - kg item pair dict'''
    reversed_dict=defaultdict(list)
    dict_1={key:set(values) for key,values in dict_1.iteritems()}
    dict_1=defaultdict(set,dict_1)
    #print extra_items_dict
    for key,values in extra_items_dict.iteritems():
        for value in values:
            reversed_dict[value].append(key)
    reversed_dict={key:list(set(values)) for key,values in reversed_dict.iteritems()}
    #print "THe reversed_dictionary",reversed_dict
    
    for key,item in reversed_dict.iteritems():
        #print item
        dict_1[key].update(item)

    dict_1={key:list(set(values)) for key,values in dict_1.iteritems()}
    return dict_1

def readable_kegg_wrapper(kegg_item,extra_items,database_dir):
    '''Adds the user specified extras to the existing readable database after it is loaded into python.'''
    
    readable_names=load_readable_names(database_dir,[kegg_item],False)[kegg_item]
    if extra_items==None:
        pass
    else:
        for key in extra_items.iterkeys():
            readable_names[key]=key    
    return readable_names
    
def load_counts_file(totals_file):
    total_counts=pd.Series(pd.read_table(totals_file,sep="\t",header=None,index_col=0))
    return total_counts
    
def identify_tests(comparison_dict,groupings):
    '''Identifies if comparisons are going to be for individuals or groups.
    Input:
    
    Output:
    
    '''
    test_type={}
    for baseline_group,targets in comparison_dict.iteritems():
        for target in targets:
            if target in groupings:
                if baseline_group in groupings:
                    test_type[(baseline_group,target)]="G-G"
                else:
                    test_type[(baseline_group,target)]="I-G"
            else:
                if baseline_group in groupings:
                    test_type[(baseline_group,target)]="G-I"
                else:
                    test_type[(baseline_group,target)]="I-I"
                    
    return test_type

def make_KO_set_from_series(KO_series):
    
    return set(KO_series[KO_series>0].index)
    
def load_definition_file(def_file):
    def_dict={}
    with open(def_file) as definitions:
        for line in definitions:
            module,definition=line.strip().split("\t")
            def_dict[module]=definition
    return def_dict

def make_extra_definition_database(definitions_file,database_dir):
    '''
    Definition:
        This function will take an entire kegg module definition file and will create
        a new local database with the expressions written so that they can simple be
        evaluated when loading the files.
    Input: 
        database_dir: str
            A directory containing the database of kegg module definitions.
    Output:
        None
    Calls:
        replacement: Turns kegg definitions in logical nested tuples of sets.
    '''
    #print "THe definitions file", definitions_file
    old_module_def=load_definition_file(definitions_file)
    #print old_module_def
    #print "This is the old module information",old_module_def
    new_pd_df=[""]*len(old_module_def)
    i=0
    for module,definition in old_module_def.iteritems():
        #print module, definition
        try:
            logical_evaluation=replacement(definition,False)[1]
            #print module, logical_evaluation
            new_pd_df[i]=[module,logical_evaluation]
            i+=1
                
        except TypeError:
            print "TypeError 2:",module,";", definition
        except SyntaxError:
            print "SyntaxError 2:",module,";", definition
        except NameError:
            print "NameError 2:",module,";" ,definition
    #print new_pd_df      
    new_pd_df=pd.DataFrame(new_pd_df)
    #print "The second checkpoint."
    #print new_pd_df
    new_pd_df.columns=["ModuleID","KEGG_log_expr"]

    new_pd_df.to_csv(os.path.join(database_dir, "module_extra_kegg_log_expr.tsv"),header=True,sep="\t",index=False)
    
    return None

def load_local_cleaned_definition_db(extra_def_file):
    cleaned_db={}
    with open(os.path.join(extra_def_file)) as paired_exprs:
        next(paired_exprs) #Skip header
        for line in paired_exprs:
            module,expr=line.split("\t")
            kegg_log=eval(expr)
            if not isinstance(kegg_log,tuple):
                kegg_log=tuple([kegg_log])
            cleaned_db[module]=kegg_log
    return cleaned_db

def logical_loading_wrapper(database_dir, definitions_file, extras):
    '''
    Loads the kegg booleans used to determine the completeness of a module.
    It can also handle creating a database for the user added definitions and loading them at the same time
    as the complete kegg directory.
    
    Input:
    databse_dir: str
        location of database files
    definitions_file: str or None
        location of user definition definitions
    extras: dict or None
        The extra modules added by the user with no definition structure.
    Output:
        original_kegg_log : dict
            module,kegg_boolean pairs to be used for completeness evaluations
    
    '''
    if definitions_file!=None:
        print "Using predefined kegg booleans"
        make_extra_definition_database(definitions_file,database_dir)
        original_kegg_log=load_local_cleaned_definition_db(os.path.join(database_dir,"module_kegg_log_expr.tsv"))
        new_kegg_log=load_local_cleaned_definition_db(os.path.join(database_dir, "module_extra_kegg_log_expr.tsv"))
        for module, kegg_bool in new_kegg_log.iteritems():
            original_kegg_log[module]=kegg_bool
            #print kegg_bool
    elif definitions_file==None and extras!=None:
        print "Automatically creating kegg boolean from module components"
        make_extras_logical(definitions_file,extras,database_dir)
        original_kegg_log=load_local_cleaned_definition_db(os.path.join(database_dir,"module_kegg_log_expr.tsv"))
        new_kegg_log=load_local_cleaned_definition_db(os.path.join(database_dir, "module_extra_kegg_log_expr.tsv"))
        for module, kegg_bool in new_kegg_log.iteritems():
            original_kegg_log[module]=kegg_bool
            #print kegg_bool
    else:
        print "No extra definitions have been added."
        original_kegg_log=load_local_cleaned_definition_db(os.path.join(database_dir,"module_kegg_log_expr.tsv"))
        
    return original_kegg_log
