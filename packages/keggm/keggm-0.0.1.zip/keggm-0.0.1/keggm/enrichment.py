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

from kegg_core import *
from multtestcorrection import *
from completeness import *
import os, sys
from collections import defaultdict
import scipy.stats
import pandas as pd

def split_results_comparison(enrichment_results):
    '''Splits the result dataframe into those for which a test was conducted and
    those where no test was conducted.'''
    split_frames={}
    #["pathway","pvalue",'expectedcount','observedcount',"completeness"]
    split_frames["tested"]=enrichment_results[:][(enrichment_results.expectedcount>0) & (enrichment_results.observedcount>0)]
    split_frames["untested"]=enrichment_results[:][~(enrichment_results.expectedcount>0) & (enrichment_results.observedcount>0)]
    
    return split_frames
    
def construct_overlap_file(comparison_dict, groupings):
    groupings={key: set(members) for key, members in groupings.iteritems()}
    groupings=defaultdict(set,groupings)
    #print groupings
    overlap_dict={}
    for source, targets in comparison_dict.iteritems():
        for target in targets:
            if target in groupings:
                if source in groupings:
                    overlap_dict[(target,source)]=list(groupings[source] & groupings[target])
                else:
                    overlap_dict[(target,source)]=list(set([source]) & groupings[target])
            else:
                if source in groupings:
                    overlap_dict[(target,source)]=list(groupings[source] & set([target]))
                else:
                    overlap_dict[(target,source)]=list(set([source]) & set([target]))
                    
        
    return overlap_dict

def write_enrichment_data(enrichment_results_dict,database_dir,output_dir,bin_taxa,mult_adjust,extras_items):
    '''Writes the Results_dict from the all_comparisons function after turning them into a pandas
    dataframe'''
    #readable_orthology=readable_kegg_wrapper("orthology",extra_items,database_dir)
    readable_orthology=load_readable_names(database_dir,["orthology"],False)["orthology"]
    readable_kegg_items=readable_kegg_wrapper("module",extras_items,database_dir)
    #readable_kegg_items=load_readable_names(database_dir,["Module"],False)["Module"]
    
    for key,df in enrichment_results_dict.iteritems():
        df.index.set_names(['target','source'],inplace=True)
        df.reset_index(inplace=True)
        df["readable_name"]=df["pathway"].map(readable_kegg_items)
        df["readable_target"]=df["target"].map(bin_taxa)
        df.to_csv(os.path.join(output_dir,"enriched_{0}_corrected_{1}_comparisons.tsv".format(key,mult_adjust)),sep="\t",index=False)
    #pandas_dataframes["Module"]={}
   
    return enrichment_results_dict


def adjusted_enrichment_test(target, source,threshold,MO_hits,database_dir,KO_KG_ITEM_PAIRS,KG_ITEM_KO_PAIRS,KO_PTH_structure,total_KO_hits,KO_hits,overlap_dict,comp_type,groupings,kegg_item="Module"):
    '''A simple test for enrichment of some kegg item in the target genome based on the baseline probabilities calculated using
    the source genome. A simple binomial test is used to work out the probably of seeing as many genes as was present
    in the target genome given that it has the same chance of occuring as in the source genome. All module present in the
    target but not at all in the source are also included in the output as (0,0,observed count of kegg item,0).f
    
    Input: 
        target               -  Genome to investigate for enrichment
        source               -  The genome used to calculate the baseline chance of a kegg_item occuring.
        KO_hits              -  Dictionary of genome: KO pairs, requires a collated entry for all microorganisms
        threshold            -  The significance threshold before corrections.
        kegg_item            -  The kegg_item to look for enrichment of. Normally run as [module, pathway]
        database_dir         -  The location of the linking files and file descriptions
    Output:
        enrichment_scores    -  p value, expected hits, observed hits, completeness score'''
    

    shared_pathways=MO_hits.ix[(MO_hits.loc[:,source]>0) & (MO_hits.loc[:,target]>0),:].index


    all_target_KOs=make_KO_set_from_series(KO_hits[target])
    all_source_KOs=make_KO_set_from_series(KO_hits[source])
    #print "Number of unique KOs present for the target.", target, len(all_target_KOs)
    target_KOs={PTH:set(items) & all_target_KOs  for PTH, items in KG_ITEM_KO_PAIRS.iteritems()}
    target_KOs=defaultdict(set,target_KOs)
    source_KOs={PTH:set(items) & all_source_KOs  for PTH, items in KG_ITEM_KO_PAIRS.iteritems()}
    source_KOs=defaultdict(set,source_KOs)
    
    #print "This is the source and target", source, target
    
    #Eventually this should be provided by the user
    
    enrichment_scores=defaultdict(lambda:(0,0,0,0))
    
    #print "These were the overlapping organisms", overlap_dict[(target,source)]

    account_for_overlap=isinstance(overlap_dict,dict)
    if account_for_overlap:
        overlapped_hits=MO_hits[overlap_dict[(target,source)]].sum(axis=1)
        overlap_free_source=MO_hits[source]-overlapped_hits
    else:
        overlap_free_source=MO_hits[source]
    #print overlap_free_source
    #print "weird value", MO_hits[source]['Msuper_duper']
    #print "weird value", MO_hits[target]['Msuper_duper']
    #print "The negative values",overlap_free_source[overlap_free_source<0]
    #
    #Branching process to decide the best statistical test and prep for
    #if 
    #
    
    
    #print "The total number of KOs for source and target,", N_source_KOs, N_target_KOs
    if comp_type=="I-I":
        #Get totals
        N_source_KOs=total_KO_hits[source]
    
        N_target_KOs=total_KO_hits[target]
        #Do fisher's exact test
        for PTH,count in MO_hits[target].iteritems():
            if pd.isnull(count):
                print PTH, count, target,source
            if PTH in shared_pathways:

                cont_tab_test=scipy.stats.fisher_exact
                N_source_PTH_hits=overlap_free_source[PTH]
                p_PTH_source=float(N_source_PTH_hits)/N_source_KOs
                data_table=[[count,N_source_PTH_hits],[N_target_KOs-count,N_source_KOs-N_source_PTH_hits]]
                #print PTH, data_table,N_source_KOs, N_source_PTH_hits
                p_val=cont_tab_test(data_table)[1]



            else:
                cont_tab_test=lambda x: 0
                N_source_PTH_hits=0
                p_PTH_source=0
                data_table=[[count,N_source_PTH_hits],[N_target_KOs-count,N_source_KOs-N_source_PTH_hits]]
                #print data_table
                p_val=cont_tab_test(data_table)

            enrichment_scores[PTH]=(p_val,p_PTH_source*N_target_KOs,count,new_measure_completeness(PTH,target_KOs[PTH],KO_PTH_structure[PTH],True))
        return enrichment_scores
    elif comp_type=="G-I":
        #Get totals
        N_source_KOs=total_KO_hits[groupings[source]]
    
        N_target_KOs=total_KO_hits[target]
        #Extract background
        background=MO_hits.loc[:,groupings[source]]
        #print background
        background=background.div(N_source_KOs,axis='columns')
        #print background.sum(axis='rows')
        exp_count=background.mean(axis='columns')*N_target_KOs
        #Group by pathway and extract mean and std deviation
        means=background.mean(axis=1)
        stds=background.std(axis=1)
        #Get p-values from test
        obs_count=MO_hits.loc[:,target]
        observed=obs_count.divide(N_target_KOs)
        obs_Zscore=((observed-means)/stds).abs()
        #Z-test to see chance of individual as different as observed
        p_obsgbg=pd.Series(2-2*scipy.stats.norm.cdf(obs_Zscore),index=observed.index)
        #p_obsgbg
        #print "p-values",p_obsgbg
        
        completeness_func=lambda PTH: new_measure_completeness(PTH,target_KOs[PTH],KO_PTH_structure[PTH],True)
        completeness_scores=pd.Series(background.index.map(completeness_func),index=background.index)
        #Need to measure completeness now
        #print type(p_obsgbg)
        #print type(exp_count)
        #print type(obs_count)
        #print type(completeness_scores)
        new_df=pd.concat([p_obsgbg,exp_count,obs_count,completeness_scores],axis=1)
        new_df.columns=["pvalue",'expectedcount','observedcount',"completeness"]
        #temporarily fill nas with 0s
        new_df.fillna(0,inplace=True)
        #print "joined df",new_df
        #print new_df.shape
        return new_df
    elif comp_type=="I-G":
        #Get totals
        #print total_KO_hits.index
        N_source_KOs=total_KO_hits[source]
    
        N_target_KOs=total_KO_hits[groupings[target]]
        #need to flip
        background=MO_hits.loc[:,groupings[target]]
        background=background.div(N_target_KOs,axis='columns')
        #print background.sum(axis='rows')
        exp_count=background.mean(axis='columns')*N_source_KOs
        #print exp_count
        #Group by pathway and extract mean and std deviation
        means=background.mean(axis=1)
        stds=background.std(axis=1)
        #Get p-values from test
        obs_count=MO_hits.loc[:,source]
        observed=obs_count.divide(N_source_KOs)
        
        obs_Zscore=((observed-means)/stds).abs()
        #Z-test to see chance of individual as different as observed
        p_obsgbg=pd.Series(2-2*scipy.stats.norm.cdf(obs_Zscore),index=observed.index)
        #print "p-values",p_obsgbg
        
        completeness_func=lambda PTH: new_measure_completeness(PTH,source_KOs[PTH],KO_PTH_structure[PTH],True)
        completeness_scores=pd.Series(background.index.map(completeness_func),index=background.index)
        
        #Form all results back to a dictionary of tuples
        #print type(p_obsgbg)
        #print type(exp_count)
        #print type(obs_count)
        #print type(completeness_scores)
        new_df=pd.concat([p_obsgbg,exp_count,obs_count,completeness_scores],axis=1)
        new_df.columns=["pvalue",'expectedcount','observedcount',"completeness"]
        #temporarily fill nas with 0s
        new_df.fillna(0,inplace=True)
        #print "joined df",new_df
        #print new_df.shape
        return new_df
    elif comp_type=="G-G":
        #t-test to see difference in proportions
        #print target, source
        
        N_source_KOs=total_KO_hits[groupings[source]]
    
        N_target_KOs=total_KO_hits[groupings[target]]
        
        background=MO_hits.loc[:,groupings[source]].div(N_source_KOs,axis='columns')
        #
        obs_count=MO_hits.loc[:,groupings[target]]
        test=obs_count.div(N_target_KOs,axis='columns')
        obs_count=obs_count.mean(axis='columns')
        #
        exp_count=background.mean(axis='columns')
        #print exp_count.shape
        exp_count=exp_count*N_target_KOs.mean()
        #print exp_count.shape
        #Do two sample t-test on each pathway
        #print test.shape
        #print background.shape
        t_stats,pvals=scipy.stats.ttest_ind(background,test,axis=1,equal_var=False,nan_policy='raise')
        #print pvals
        pvals=pd.Series(pvals,index=background.index)
        #print len(pvals)
        #Still need to calculate completeness score
        completeness_func=lambda PTH: 0
        completeness_scores=pd.Series(background.index.map(completeness_func),index=background.index)
        #Form all results back to a dictionary of tuples
        #print type(pvals),pvals.index
        #print type(exp_count),exp_count.index
        #print type(obs_count),obs_count.index
        #print type(completeness_scores),completeness_scores.index
        new_df=pd.concat([pvals,exp_count,obs_count,completeness_scores],axis=1)
        new_df.columns=["pvalue",'expectedcount','observedcount',"completeness"]
        #temporarily fill nas with 0s
        new_df.fillna(0,inplace=True)
        #print "joined df",new_df
        #print new_df.shape
        #print new_df

        return new_df
        
def do_enrichment_comparisons(KO_hits, threshold, database_dir, comparisons,extras_dict,excluded_set,definition_file,overlap_dict,make_mo_comp,groupings,total_counts=None):
    '''Makes all of the enrichment comparisons specified in comparisons.
    Input:
    
    Output:
    '''
    #print "Inside do_enrichment_comparison this is the extras_dict", extras_dict
    results_dict={}
    
    if make_mo_comp:
        #Load pairings
        KO_KG_ITEM_PAIRS=kegg_pairs_wrapper(["orthology","module"],excluded_set, extras_dict,database_dir)
        #KO_KG_ITEM_PAIRS=load_local_kegg_database_pairings(database_dir,[("orthology",kegg_item)], False)[("orthology",kegg_item)]
        KO_KG_ITEM_PAIRS=defaultdict(set, KO_KG_ITEM_PAIRS)
        #KG_ITEM_KO_PAIRS=load_local_kegg_database_pairings(database_dir,[(kegg_item,"orthology")], False)[(kegg_item,"orthology")]
        KG_ITEM_KO_PAIRS=kegg_pairs_wrapper(["module","orthology"],excluded_set, extras_dict,database_dir)
        KG_ITEM_KO_PAIRS={MO:list(set(KOs)) for MO,KOs in KG_ITEM_KO_PAIRS.iteritems()}
        #Must be MODULES
        KO_PTH_structure=logical_loading_wrapper(database_dir, definition_file, extras_dict)
        #KO_PTH_structure=load_local_cleaned_definition_db(database_dir)
        KO_PTH_structure=defaultdict(tuple,KO_PTH_structure)
        if isinstance(total_counts,type(None)):
            total_KO_hits=KO_hits.sum(axis=0)
        else:
            total_KO_hits=total_counts
        if isinstance(KG_ITEM_KO_PAIRS,type(None)):
            print database_dir
        if isinstance(KO_KG_ITEM_PAIRS,type(None)):
            print database_dir
        #print total_KO_hits
        #print total_KO_hits
        new_MO_hits_matrix=construct_MO_matrix(KO_hits, KG_ITEM_KO_PAIRS)

        
        #Add totals in here somewhere
        
        
    else:
        KO_KG_ITEM_PAIRS=None
        KG_ITEM_KO_PAIRS=None  
        KO_PTH_structure=None
        if isinstance(total_counts,type(None)):
            total_KO_hits=KO_hits.sum(axis=0)
        else:
            total_KO_hits=total_counts
        #print total_KO_hits
        new_MO_hits_matrix=KO_hits
        #print "NEw extreme values", new_MO_hits.ix[(new_MO_hits>total_KO_hits).any(axis=1),:]
        #print "weird value", new_MO_hits_matrix.loc['Msuper_duper',:]
    print "Option to make module comparisons", make_mo_comp
    for (source, target),comp_type in comparisons.iteritems():
#        for target in targets:
        result=adjusted_enrichment_test(target,source,threshold, new_MO_hits_matrix,database_dir,KO_KG_ITEM_PAIRS,KG_ITEM_KO_PAIRS,KO_PTH_structure,total_KO_hits,KO_hits,overlap_dict,comp_type,groupings)
        if len(result)>0:
            #print results
            if isinstance(result,pd.DataFrame):
                #move pathway index to column
                result.reset_index(level=0, inplace=True)
                results_dict[(target,source)]=result
            else:
                result=pd.DataFrame.from_dict(result,orient="index")
                #print result
                #Completeness for custom modules wasn't working and there were some nans
                result.reset_index(level=0, inplace=True)
                results_dict[(target,source)]=result
    
    results_dict=pd.concat(results_dict.values(), keys=results_dict.keys())
    #print results_dict
    results_dict.columns=["pathway","pvalue",'expectedcount','observedcount',"completeness"]
    results_dict.index=results_dict.index.droplevel(level=-1)

    return results_dict

def construct_MO_matrix(KO_hits, KG_ITEM_KO_PAIRS):
    '''Constructs a new matrix with hits per module to use for enrichment tests.
    Input:
        KO_hits             -    pandas df of KO hits
        KG_ITEM_KO_PAIRS    -    mapping between KOs and modules
    Output:
        new_module_df       -    Number of genes belonging to each module'''
    
    new_module_counts={}
    
    all_seen_KOs=set(KO_hits.index)
    
    for Module, KOs in KG_ITEM_KO_PAIRS.iteritems():
        #print KOs
        hits_per_module=KO_hits.ix[KOs,:].sum(axis=0)
        
        #Check if NaNs are happening when KOs are there
        if len(set(KOs) & all_seen_KOs)==0:
            hits_per_module.fillna(0,inplace=True)
        elif hits_per_module.isnull().any():
            raise TypeError
        #print hits_per_module
        #print "Module", Module, hits_per_module['coral']
        new_module_counts[Module]=hits_per_module
    #print "weird_coral_stuff",sum(KO_hits['coral']), KO_hits['coral']
    new_module_df=pd.DataFrame.from_dict(new_module_counts,orient='index')
    #print new_module_df
    return new_module_df
