"""
This scripts aims to extract the following information from the gold RSTDT .rsd files
	1. # Number of dependency children in the gold graph (direct)
	2. # Number of dependency descendants in the gold graph (indirect, i.e. recursive dependency count)
"""

import os
import io
from collections import defaultdict, Counter


script_dir = os.getcwd()
data_dir = script_dir.replace("utils", "data") + os.sep + "RSTDT" + os.sep

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
