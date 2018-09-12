import sys
import os
import pickle
import pandas
import numpy as np

from ontobio.ontol_factory import OntologyFactory
from ontobio.assoc_factory import AssociationSetFactory



HUMAN = 'NCBITaxon:9606'

#ontology paths
##''/Users/marcin/Documents/VIMSS/ontology/NCATS/HPO/hp.obo')#mondo#hp

ofactory = OntologyFactory()
afactory = AssociationSetFactory()
print("creating...")
ont = ofactory.create('hp')
#ont = ofactory.create('mondo')
aset = afactory.create(ontology=ont,
                       subject_category='disease',
                       object_category='phenotype',
                       taxon=HUMAN)

###aset = afactory.create_from_gaf('my.gaf', ontology=ont)

                
disease_ids = ["DECIPHER:1", "DECIPHER:16", "OMIM:614696", "OMIM:614699", "Orphanet:99978"]
phenotype_ids = ["HP:0000007", "Orphanet:93299", "Orphanet:90794"]
print("annotations\t"+phenotype_ids[1])

print(aset.annotations(phenotype_ids[1]))
#print(ont.equiv_graph())



#sys.exit()
                
all_disease_ids = disease_ids

#print(disease_ids)

enr = aset.enrichment_test(subjects=disease_ids, background=all_disease_ids, threshold=1, labels=True)

print(enr)





bg_file = open("disease__by__HPO_matrix_v3_yids.txt", "r")
bg_data = bg_file.read().split('\n')

del bg_data[-1]
#print(bg_data)
#print(type(bg_data))
#sys.exit()


phenotype_labels_df= pandas.DataFrame.from_csv("phenotype_labels_v2.txt", sep='\t') 
#print(phenotype_labels_df["label"])
#sys.exit()


#print(sys.argv)
#print(sys.argv[1])

#print(os.listdir(sys.argv[1]))

files = [f for f in os.listdir(sys.argv[1])]
#print(files)

for f in files:
	if f.endswith("colorder.txt"):
		print(f)
		text_file = open(sys.argv[1]+"/"+f, "r")
		lines = text_file.read().split('\n')
		print(lines)
		#print(" len(lines) " + str( len(lines)))
		
		curids = [None] * (len(lines)-1)
		#print("len(curids) "+ str(len(curids)))
		count = 1
		for l in range(1, len(lines)-1):
			s = lines[l]
			#print(s)
			split = s.split('\" \"')
			#print("split")
			#print(len(split))
			#print(split)
			#print(split[1])
			curids[count] = split[1].replace("\"","")
			count = count+1
			
#		curids = curids[-1]
		curids.pop(0)
		print(type(curids))
		print(len(curids))
		print("curids "+str(curids))

		bicluster_phenotype_ids = []
		for k in range(0, len(curids)):
			print(curids[k])
			#print(phenotype_labels_df["id"][1])
			#print(type(phenotype_labels_df["id"] ))

			#innerindex = (phenotype_labels_df["id"] == phenotype_ids[k].replace(".",":"))
			innerindex = (phenotype_labels_df["label"] == curids[k])
	
			#print(innerindex)
	
			whichisit = np.nonzero(innerindex == True)
			#print("whichisit")
			#print(whichisit)
			#print(len(whichisit))
	
			done = False
	
			if whichisit is not None and len(whichisit) > 0:
				#print("ADDING")
				#print(whichisit)	
				#print(type(whichisit[0]))
				keys = list(phenotype_labels_df["id"][whichisit[0]])
				if(len(keys) > 0):
					#print(keys)
					#print(keys[0])
					#print(phenotype_labels_df["label"][whichisit[0]])
		
					bicluster_phenotype_ids.append(keys[0])
					done = True
			#else:
			#	bicluster_phenotype_labels.append("none")
		
			#print(done)
			#if not done:
				#print("NONE")
				#bicluster_phenotype_ids.append("none")	
		
		print(bicluster_phenotype_ids)		
		print(bg_data[1:10])
		enr = aset.enrichment_test(subjects=bicluster_phenotype_ids, background=bg_data, threshold=1, labels=True)

		print(enr)
		sys.exit()