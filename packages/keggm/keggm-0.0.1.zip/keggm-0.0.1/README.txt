Keggm - a small suite of tools I use to analyses microbial genomes

This is currently a very barebones package. Only two functions are fully operational.

enrichm looks for metabolic blocks which are enriched in your genomes compared to some background.
This is good to try and get a quick idea on how your genomes are different to the background set in terms of certain metabolic functions.
You can specify you own blocks and use custom protein names which make it quite extensible.

completm is a small tool to aid exploring what functions your genome can perform.
It creates a "completeness" matrix which gives you an idea if your genome shows the potential to perform that metabolic block.
It also create a matrix with the protein names which contributed to that completeness which can help you check if your metabolic block was
complete due to proteins which are normally poorly annotated and, if there are complementary proteins, which ones were present.
This will be expanded to provide a list of "complete" modules for each organism based on some user threshold.


*In the works*

plots aims to create some small visualisations to better parse the completeness results. It consists of heatmaps, to quickly scan across genomes, 
and will later included arrows diagrams of each metabolic block where each arrow represents a protein. 
The arrows will be coloured based on the organisms which had the relevant proteins.

overlap tries to identify is organisms have the potential to supplement each other. 
It does this by looking for metabolic blocks which are complete in one organisms but the rests of the metabolic block can be found in another organism.

TODO:

1. Make a better test suite
	
2. Make it usable on the command line (for convenience)

3. Implement auxilliary non-enrichment features into main software
	a. Plots with options to compare completeness
	b. Visualisation of overlap within module across multiple genomes similar to Symbiodinium+coral paper
	c. Some kind of colourisation of KEGG pathways to give you a broad idea of what's present within a pathway.

4. Eventually, if I can, make the network stuff robust enough for the potential automated discovery of novel metabolism

5. Add more customisability - Make it that any user can essentially create there own extra kegg data for use in this software
	a. requires a few auxilliary tools to augment permanent databases

6. Unify Database scraping and production to be a single command

-----------------------------------------------------------------------------------------------------------------------------

Other todo:

1. Make it multithreaded/multiprocessor at the comparison stage (current scale of comparisons poses no speed issue)
	Implement in terms of producure consumer model of multithreading

2. Investigate optimised Booschloo's test and if it has reasonable runtime (unlikely)

3. Implement a logging system for better debugging - will make my life easier.