"""
This scripts aims to extract the following information from the gold .rsd files
	1. # Number of dependency children in the gold graph (direct)
	2. # Number of dependency descendants in the gold graph (indirect, i.e. recursive dependency count)
"""

import os
import io
from collections import defaultdict, Counter


script_dir = os.getcwd()
data_dir = script_dir.replace("utils", "data") + os.sep + "GUM9" + os.sep

# directories for rsd files from GUM test
human_dir = data_dir + "human" + os.sep

# initialize a document-level dict to store dependency-related information
dep_direct_dict = defaultdict()
edu_dep_dict = defaultdict(defaultdict)

for file in os.listdir(human_dir):
	if file.endswith(".rsd"):
		filename = file.split(".")[0]
		lines = io.open(os.path.join(human_dir, file), "r", encoding="utf-8").read().strip().split("\n")

		dep_ids = []
		for line in lines:
			if "\t" in line:
				fields = line.split("\t")
				edu_idx = int(fields[0])
				edu_dep = int(fields[6])
				dep_ids.append(edu_dep)

				if fields[7] == "ROOT":
					ROOT_EDU = edu_idx

				edu_dep_dict[filename][edu_idx] = edu_dep

		# get the number of direct child
		dep_direct_dict[filename] = Counter(dep_ids)


def trial():
	# direct
	# print(dep_direct_dict["GUM_voyage_vavau"])

	# indirect
	sample_indirect_dict = edu_dep_dict["GUM_academic_discrimination"]
	dep_descendant_list_doc_level = []
	for edu_id in sample_indirect_dict:
		dep_descendant_list = []
		temp = sample_indirect_dict[edu_id]
		while temp != 0:
			dep_descendant_list.append(temp)
			temp = sample_indirect_dict[temp]

		# print(dep_descendant_list)
		if len(dep_descendant_list) == 2:
			dep_descendant_list_doc_level.append(dep_descendant_list[1])
		elif len(dep_descendant_list) > 2:
			dep_descendant_list_doc_level += dep_descendant_list[1:]

	print(Counter(dep_descendant_list_doc_level))
