#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json

data=json.load(open('everyProtein.json','r'))

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

results=[]

exosome= open('VESICLEPEDIA_PROTEIN_MRNA_DETAILS_4.1.txt','r')
exosomeData=exosome.readlines()
#print(exosomeData)
#\t between 1 and 2 for protein/mRNA, third \t for protein name
for line in exosomeData:
    #verify whether protein or RNA
    start=line.find('\t')
    end=find_nth(line,"\t",2)
    classification=line[start+1:int(end)]
    
    #determine whether it comes from human or not
    sHuman=find_nth(line,"\t",4)
    eHuman=find_nth(line,"\t",5)
    isHuman=line[sHuman+1:int(eHuman)]
    #print(isHuman)
    if(classification=='protein' and isHuman=='Homo sapiens'):
        #extract name of protein
        s=find_nth(line,"\t",3)
        e=find_nth(line,"\t",4)
        name=line[s+1:e]
        results.append(name)
        
polishedResults=set(results)
print(polishedResults)

for thing in polishedResults:
    #two nested for loops cycling through the database for each one
    for object in data:
    #nest region specificity and location in vesicles
        holder=object.get('Subcellular location')
        brainHolder=object.get('RNA brain regional specificity')
        cellLocation=object.get('Protein class')
        if object.get('Gene')==thing:
            if holder is not None and 'Vesicles' in holder:
                if (brainHolder!= 'Low region specificity' and brainHolder!= 'Not detected' and brainHolder is not None) or (object.get('RNA brain regional distribution') == 'Detected in single'):
                    if 'Predicted membrane proteins' in cellLocation:
                        print(object.get('Gene')+ '       '+object.get('RNA brain regional specificity') +'        '+object.get('RNA brain regional distribution'))
    

