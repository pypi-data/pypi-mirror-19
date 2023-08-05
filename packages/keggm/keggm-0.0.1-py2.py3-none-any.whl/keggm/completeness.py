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
#
###############################################################################

from collections import defaultdict
import re
import itertools
import numpy as np
import pandas as pd
import kegg_core
import enrichment


def replacement(definition,return_string=False):
    '''
    Description:
        Turns an irregular definition string into a set of KOs in nested tuples to indicate their relationship and to
        prepare them for processing.
    Input:
        definition: string
            Module definition as defined in KEGG    
    output:
        definition: Same as above
        new_nesting: tuple of tuples of sets
            The new logical form of the definition to use in evaluating completeness.
        
    Notes: 
        This function uses eval which a security risk. Caution should be taken in using this function
    '''
    
    logical_chars="[+ ,-]"
    pattern="K[0-9]{5}"
    new_expression=definition
    logical_groups="([K][0-9]+,){1,}[K][0-9]+" #Find any group of KOs (1 or more) separated by commas
    #non_extended_groups='(K[0-9]{5}[^,K0-9\n\]]*){1,}(K[0-9]{5}[^,])' #Get any none comma separated chunk of KOs
    non_extended_groups='([^,]|^)(K[0-9]{5}[^,K0-9\n\]\)\[]*){1,}([\n \+\"\]\[\(\)]|$)'
    end_KOs='(K[0-9]{5})$'
    repeated_set='(set\(\[){2,}(["][K][0-9]+["][^^ )(+.\"-]?).*?(\]\)){1,2}'
    set_in_set='set\(\[[K0-9",]*(set\(\[)"[K][0-9]+"\]\)'
    rear_match="([^0-9][,-]K[0-9]{5})"
    forward_match='(K[0-9]{5})[,-][\(]'
    new_expression=new_expression.replace(" -","-")
    new_expression=new_expression.replace(", ",",")
    ko_set_matches=[]
        
    for match in re.finditer(logical_groups,new_expression):
        #print match.group()
        ko_set_matches.append(match.group())
        #new_expression=new_expression.replace(match.group(),"set(["+match.group()+"])",1)
    set_matches=['']*len(ko_set_matches)
    cleaned_matches=[match.strip(",") for match in ko_set_matches]
    ko_set_matches=set(cleaned_matches)
    
    
    for i,match in enumerate(ko_set_matches):
        set_matches[i]=match
        new_expression=new_expression.replace(match,"set(["+match+"])")
        
    step_0_1=new_expression
    for match in re.finditer(non_extended_groups,new_expression):
        if match:
            new_match=match.group()
            #print type(new_match), new_match
            for sub_match in re.findall(pattern,new_match):
                new_match=new_match.replace(sub_match,"set(["+sub_match+"])")
            new_expression=new_expression.replace(match.group(),new_match)
            
    for match in re.finditer(rear_match,new_expression):
        if match:
            new_match=match.group()
            #print type(new_match), new_match
            for sub_match in re.findall(pattern,new_match):
                new_match=new_match.replace(sub_match,"set(["+sub_match+"])")
            new_expression=new_expression.replace(match.group(),new_match)
            
    for match in re.finditer(forward_match,new_expression):
        if match:
            new_match=match.group()
            #print type(new_match), new_match
            for sub_match in re.findall(pattern,new_match):
                new_match=new_match.replace(sub_match,"set(["+sub_match+"])")
            #print new_match
            new_expression=new_expression.replace(match.group(),new_match)
                
    step_0_2=new_expression
    for match in set(re.findall(pattern,new_expression)):
        new_expression=new_expression.replace(match,"\""+match+"\"")
    step_1=new_expression
    #print new_expression
    
    new_expression=new_expression.replace(",",",\",\",")
    #non_set_comma='.{6}[^\"],[^\"].{6}' #Extends sides to try and ensure uniqueness
    #for match in set(re.findall(non_set_comma,new_expression)):
    #    new_expression=new_expression.replace(match,",\",\",".join(match.split(",")))
        
    new_expression=new_expression.replace(" ",",\" \",")
    #print new_expression
    new_expression=new_expression.replace("-",",\"-\",")
    new_expression=new_expression.replace("+",",\"+\",")
    step_2=new_expression
    #print new_expression
    new_expression=new_expression.replace("\"\"","\"")
    new_expression=new_expression.replace(",,",",")
    new_expression=new_expression.replace(",]","]")
    new_expression=new_expression.replace(",)",")")
    new_expression=new_expression.replace("\"\"","\"")
    step_3=new_expression
    #No Longer needed due to fix in tests.

    for match in re.finditer(repeated_set,new_expression):
        #print "This is the match", match.group()
        new_match=match.group().strip("set([")
        new_match=new_match.strip("])")
        new_match="set(["+new_match+"])"
        #print
        #print "This is the new match", new_match
        new_expression=new_expression.replace(match.group(),new_match)
    
    for match in re.finditer(set_in_set,new_expression):
        new_match=match.group()
        #print new_match.split("set([")
        blank, section_1,section_2=new_match.split("set([")
        section_2=section_2.strip("])")
        #print section_2
        new_match="set(["+section_1+section_2
        new_expression=new_expression.replace(match.group(),new_match)
    step_4=new_expression
    isolated_start="^\"K[0-9]{5}\""
    for match in re.findall(isolated_start,new_expression):
        new_expression=new_expression.replace(match,"("+match+",)")
        
    new_expression="("+new_expression+")"
    
    
        
    
    if return_string:
        #print "Made it to string"
        return new_expression
    try:
        #print "Made it to evaluations"
        new_nesting=eval(new_expression)
        return definition,new_nesting 
    

        
    except TypeError:
        print definition
        print "0_1",step_0_1
        print "0_2",step_0_2
        print "Step 1:", step_1
        print "Step 2:", step_2
        print "Step 3:", step_3
        print "Step 4:", step_4
        print ";".join(set_matches)
        print "Type error", new_expression
        raise
        
    except SyntaxError:
        print definition
        print "0_1",step_0_1
        print "0_2",step_0_2
        print "Step 1:", step_1
        print "Step 2:", step_2
        print "Step 3:", step_3
        print "Step 4:", step_4
        print ";".join(set_matches)
        print "Syntax error", new_expression
        raise
        
    except NameError:
        print definition
        print "0_1",step_0_1
        print "0_2",step_0_2
        print "Step 1:", step_1
        print "Step 2:", step_2
        print "Step 3:", step_3
        print "Step 4:", step_4
        print ";".join(set_matches)
        print "NameError", new_expression
        raise
        
    return
        
     

def alt_eval_kegg_bool(kegg_expr,ko_set):
    '''
    Description:
        Evaluates a list of boolean expressions blocks to get a list of T, F results summarising the module completeness.
    Input: 
        kegg_expr: List of sets
            A kegg expression consting of KOs in nested tuples. eg, (KO1 ((KO2,KO3-KO4),KO5).
            The separators represent the kegg boolean separators.

        ko_set: set
            The set of KOs to be evaluated for compelteness in this particular kegg expression.
    Calls:
        eval_kegg_bool: function
            The workhorse of  this function - recursively evaluates each element in kegg_expr to
            decide if it is actually true or false.
    '''
    n_elements=len(kegg_expr)
    results_vec=["na"]*n_elements
    for i in xrange(0,n_elements,2):
        current_element=kegg_expr[i]
        if isinstance(current_element,tuple):
            side_1_result=eval_kegg_bool(current_element,ko_set)
        else:
            side_1_result= len(ko_set & current_element)>0

        full_result=side_1_result
        #print full_result
        results_vec[i]=full_result
    #print results_vec
    for i,element in enumerate(results_vec):
        if not isinstance(element,bool):
            results_vec[i]=kegg_expr[i]
    
    return (n_elements+1)/2,results_vec
    
    
def eval_kegg_bool(kegg_expr,ko_set):
    '''
    Description:
        A recursive implementation of the kegg boolean logic for evaluating based on a set of KOs if a module is complete.
        If given a tuple it will recursively search down for more tuples and evaluate them at the lowest level to move up and
        finally finish evaluating the complete block. 
    Input: 
        kegg_expr: List of sets
            A kegg expression consting of KOs in nested tuples. eg, (KO1 ((KO2,KO3-KO4),KO5).
            The separators represent the kegg boolean separators.
        ko_set: set
            The set of KOs to be evaluated for compelteness in this particular kegg expression.
    Calls:
        eval_kegg_bool: function
            Evalutes logical KEGG blocks.
    '''
    n_elements=len(kegg_expr)
    #vector=np.array(["na"]*((n_element+1)/2)-1)
    for i in xrange(0,n_elements-1,2):
        #print "THe current kegg expression getting evaluated", kegg_expr[i:i+3]
        side_1,log_op,side_2=kegg_expr[i:i+3]
        #print "This is the logical operater being used",log_op
        if log_op==" " or log_op=="+":
            #print "Entering +  recursion"
            if isinstance(side_1,tuple):
                side_1_result=eval_kegg_bool(side_1,ko_set)
            else:
                side_1_result= len(ko_set & side_1)>0
            if isinstance(side_2,tuple):
                side_2_result=eval_kegg_bool(side_2,ko_set)
            else:
                side_2_result=len(ko_set & side_2)>0
            full_result=side_1_result and side_2_result
            
        elif "," in log_op:
            #print "Entering , recursion"
            if isinstance(side_1,tuple):
                side_1_result=eval_kegg_bool(side_1,ko_set)
            else:
                side_1_result= len(ko_set & side_1)>0
            if isinstance(side_2,tuple):
                side_2_result=eval_kegg_bool(side_2,ko_set)
            else:
                side_2_result=len(ko_set & side_2)>0     
            full_result=side_1_result or side_2_result
        elif "-" in log_op:
            #print "Entering - recursion"
            if isinstance(side_1,tuple):
                side_1_result=eval_kegg_bool(side_1,ko_set)
            else:
                side_1_result= len(ko_set & side_1)>0
            if isinstance(side_2,tuple):
                side_2_result=eval_kegg_bool(side_2,ko_set)
            else:
                side_2_result=len(ko_set & side_2)>0
            full_result=side_1_result
            
        else:
            print log_op, "There seems to have been an error:"
        #print "The result for side 1", side_1_result, side_1
        #print "The result for side 2", side_2_result, side_2
    #print "The final results being returned", full_result
    return full_result

def block_level_completeness(results_vector,correct_partial,nested_descr,ko_set):
    '''
    Description:
        Calculates the percent completness of a KEGG module in one of two ways. It either looks at the number of
        logical blocks complete (block level completeness) or also adds a percentage adjustment for how complete the
        incomplete blocks are.
    Input:
        results_vector: List of Booleans
            A list containing the results of evaluating a kegg module KO hits as a boolean expression.
        correct_partial: Boolean
            Indicating whether to try and account for the partial completeness of some logical blocks.
        nested_descr: nested tuple of sets
            A logical grouping of KEGG blocks into tuples with sets of KOs as the lowermost elements.
    Output:
        completeness_perc:  float in [0,1]
            Percent module completeness according to one of two methods.'''
    if isinstance(nested_descr,set):
        return len(nested_desc & ko_set) > 0
    
    keep_indices=True
    log_blocks=make_logical_blocks(results_vector,keep_indices)
    position_mapping=make_position_mapping(log_blocks)
    if keep_indices:
        log_blocks=extract_logical_values(log_blocks)
    else:
        pass
    n_tot=len(log_blocks)
    filled_blocks=[any(block) for block in log_blocks]
    n_filled_blocks=sum(filled_blocks)
    adjustment=["na"]*len(log_blocks)
    
    if not correct_partial:
        completeness_perc=float(n_filled_blocks)/n_tot
        return completeness_perc
    else:
        for i,block in enumerate(log_blocks):
            if not any(block):
                n_max_hits=len(block)
                running_total=0
                for j,item in enumerate(block):
                    if item:
                        running_total+=1
                    else:
                        bool_index=position_mapping[i][j]
                        #print "The boolean index:", bool_index
                        #print position_mapping
                        kegg_bool=nested_descr[bool_index]
                        #print kegg_bool
                        running_total+=module_completeness_proportion(kegg_bool,ko_set,correct_partial)
                adjustment[i]=float(running_total)/n_max_hits
            else:
                adjustment[i]=1    
        n_filled_blocks=sum(adjustment)
        completeness_perc=float(n_filled_blocks)/n_tot
        return completeness_perc
    
def extract_logical_values(logical_blocks):
    return [[item[1] for item in block] for block in logical_blocks]

def make_position_mapping(log_blocks):
    mapping={}
    for i, block in enumerate(log_blocks):
        mapping[i]={j:item[0] for j,item in enumerate(block)}
    #print mapping
    return mapping

def module_completeness_proportion(kegg_bool,ko_set,correct_partial):
    '''Returns the completeness of the current kegg_boolean.
    Input:
        
    Output:
        
    Calls:
        block_level_completeness: Calculate the % of kegg blocks which are complete.'''
    if isinstance(kegg_bool,set):
        return len(kegg_bool & ko_set) > 0
    #print "Kegg bool:",kegg_bool
    #print "ko_set:",ko_set
    n_el,results_vector=alt_eval_kegg_bool(kegg_bool,ko_set)
    #print "This is the result vector:",results_vector
    completeness_perc=block_level_completeness(results_vector,correct_partial,kegg_bool,ko_set)
    
    return completeness_perc
    

def make_logical_blocks(results_vector,keep_indices):
    '''
    Description:
        Turn the uppermost level of results from a KEGG boolean into a series of logical blocks. I.e if I had 
        a vector [T and F and T or F or T] then the blocks formed will be [[T],[F],[T,F,T]]. 
    Input:
        results_vector: List of Bools
            A list containing the results of evaluating a kegg module KO hits as a boolean expression.
    Output:
        log_block: list of lists of bools
            A list composed of the logical blocks needed to decide if a boolean is "complete".'''
    
    operator_set=set([" ","-",",","+"])
    log_blocks=[]
    current_block=[]
    previous_logical=""
    log_operators=[" ",",","+","-"]
    for i,item in enumerate(results_vector):
        if item not in log_operators:
            if not current_block:
                if keep_indices:
                    current_block.append((i,item))
                else:
                    current_block.append(item)
#            elif i==(len(results_vector)-1):
#                log_blocks.append(current_block)
            else:
                if previous_logical==" " or previous_logical=="+":
                    log_blocks.append(current_block)
                    if keep_indices:
                        current_block=[(i,item)]
                    else:
                        current_block=[item]
                elif previous_logical==",":
                    #print item
                    if keep_indices:
                        current_block.append((i,item))
                    else:
                        current_block.append(item)
                    #print current_block
                elif previous_logical=="-":
                    pass
        else:
            previous_logical=item
    log_blocks.append(current_block)
            
    return log_blocks
    
def new_measure_completeness(PTH,target_KOs,KO_PTH_structure,is_module):
    '''Measures completeness of possible modules. It also handles the non-module case with a 
    default of 0.'''
    if is_module:
        if KO_PTH_structure==():#empty tuple
            return 0
        else:
            perc_completeness=module_completeness_proportion(KO_PTH_structure,target_KOs,True)
            return perc_completeness
    else:
        return 0
        

def get_module_completeness(KO_hits,database_dir,excluded_items,extra_items,extra_defs_file,readable_KO_names):
    #Load pairings
    KO_KG_ITEM_PAIRS=kegg_core.kegg_pairs_wrapper(["orthology","module"],excluded_items, extra_items,database_dir)
    
    KO_KG_ITEM_PAIRS=defaultdict(set, KO_KG_ITEM_PAIRS)
    
    KG_ITEM_KO_PAIRS=kegg_core.kegg_pairs_wrapper(["module","orthology"],excluded_items, extra_items,database_dir)
    
    KO_sets=kegg_core.make_sets_from_df(KO_hits)
    
    new_MO_hits_matrix=enrichment.construct_MO_matrix(KO_hits, KG_ITEM_KO_PAIRS)
    
    observed_pathways=set(new_MO_hits_matrix.ix[new_MO_hits_matrix.apply(kegg_core.any_hits,axis=1),].index)
    print "The number of observed modules", len(observed_pathways)
    #genome_KO_PTH={genome:set(itertools.chain(*[itertools.chain(*[KO_KG_ITEM_PAIRS[KO] for KO in KOs])])) for genome,KOs in KO_hits.iteritems()}
    is_module=True
    #observed_pathways=set(itertools.chain(*[KO_KG_ITEM_PAIRS[KO] for KO in itertools.chain(*[KOs for ID, KOs in KO_hits.iteritems()])]))

    #Must be MODULES
    KO_PTH_structure=kegg_core.logical_loading_wrapper(database_dir, extra_defs_file, extra_items)            
    KO_PTH_structure=defaultdict(tuple,KO_PTH_structure)
    hit_KOs=defaultdict(lambda: defaultdict(str))
    complete_data=defaultdict(lambda: defaultdict(float))
    
    #print KG_ITEM_KO_PAIRS
    
    for genome, KOs in KO_sets.iteritems():

        for module in observed_pathways:
            cur_mod_hits=set(KOs) & set(KG_ITEM_KO_PAIRS[module])
            completeness=new_measure_completeness(module,KOs,KO_PTH_structure[module],is_module)
            #print "module", KO_PTH_structure[module]
            complete_data[genome][module]=completeness
            KO_values=list(cur_mod_hits)
            if KO_values:
                KO_values=";".join(sorted(["{0}({1})".format(readable_KO_names[KO], KO) for KO in KO_values]))
            else:
                KO_values="NoHits"
            hit_KOs[genome][module]=KO_values
            
    return complete_data,hit_KOs

def write_module_completeness_data(genome_module_data,output_file,bin_taxa,extract_core_MOs,readable_names):
    '''Creates a dataframe from the genome[module]=completeness dictionary.
    Input:
    
    Output:
    
    '''
    df=pd.DataFrame.from_dict(genome_module_data,orient='columns')
    #print "The matrix dimensions", df.shape
    #taxonomy
    #if len(bin_taxa)>0:
        #df['Taxonomy']=df.index.map(bin_taxa)
    if extract_core_MOs:
        df=df.ix[df.apply(all_hits,axis=1),]
    df['module_desc']=pd.Series(df.index,index=df.index).map(readable_names)
    #print readable_names
    #print pd.Series(df.index).map(readable_names)
    #print df['module_desc']
    cols=df.columns.tolist()
    cols=cols[-1:]+cols[:-1]
    df=df[cols]
    df.to_csv(output_file,index=True, header=True, sep="\t")
    
    return df

def write_module_ko_data(genome_ko_data,output_file,bin_taxa,readable_names):
    
    df=pd.DataFrame.from_dict(genome_ko_data,orient='columns')
    #print "The matrix dimensions", df.shape
    #taxonomy
    #if len(bin_taxa)>0:
        #df['Taxonomy']=df.index.map(bin_taxa)
    df['module_desc']=pd.Series(df.index,index=df.index).map(readable_names)
    #print readable_names
    #print pd.Series(df.index).map(readable_names)
    #print df['module_desc']
    cols=df.columns.tolist()
    cols=cols[-1:]+cols[:-1]
    df=df[cols]
    if len(set(bin_taxa.keys()) & set(df.columns.tolist()))>0:
        tuples=[df.columns.tolist(),[bin_taxa[genome_name] for genome_name in df.columns.tolist()]]
        tuples=list(zip(*tuples))
        df.columns=pd.MultiIndex.from_tuples(tuples,names=["Genome_id","Genome_taxonomy"])
    df.to_csv(output_file,index=True, header=True, sep="\t")
    
    return df
	
