"""
This script is used to extract gold annotations from GUM test files to be used for building the data table:
- token id dictionary
-
"""

import os
from collections import defaultdict


def obtain_token_ids(rsd_file):
	tokens = []
	with open(rsd_file, "r", encoding="utf-8") as f:
		for line in f.readlines():
			if "\t" in line:
				fields = line.split("\t")
				edu_txt = fields[1]
				edu_txt_tokens = edu_txt.split(" ")
				tokens += edu_txt_tokens

	token_dict = {idx+1: token for idx, token in enumerate(tokens)}

	return token_dict


def process_conllu(conllu_file, GUM=True):

	doc_dict = defaultdict(defaultdict)
	with open(conllu_file, "r", encoding="utf-8") as f_conllu:
		for idx, sent_block in enumerate(f_conllu.read().strip().split("\n\n")):
			sent_idx = idx + 1
			sent_lines = sent_block.split("\n")

			if GUM:
				# paragraph information
				if "# newpar" in sent_lines:
					new_para = "y"
				else:
					new_para = "n"
				doc_dict[sent_idx]["new_para"] = new_para

			# edu information
			doc_dict[sent_idx]["edu_ids"] = []
			for line in sent_lines:
				if "\t" in line and "Discourse=" in line:
					disc_field = line.split("\t")[9].split("|")
					for item in disc_field:
						if item.startswith("Discourse="):
							edu_id = item.split(":")[1].split("->")[0]
					doc_dict[sent_idx]["edu_ids"].append(int(edu_id))

	edu_dict = defaultdict(defaultdict)
	for sent_id in doc_dict:
		sent_dict = doc_dict[sent_id]
		edus_info = sent_dict["edu_ids"]

		if GUM:
			para_info = sent_dict["new_para"]

		if len(edus_info) == 1:
			if GUM:
				edu_dict[edus_info[0]] = {"sent_id": sent_id, "new_para": para_info, "new_sent": "y"}
			else:
				edu_dict[edus_info[0]] = {"sent_id": sent_id, "new_sent": "y"}
		else:
			if GUM:
				edu_dict[edus_info[0]] = {"sent_id": sent_id, "new_para": para_info, "new_sent": "y"}
				for edu in edus_info[1:]:
					edu_dict[edu] = {"sent_id": sent_id, "new_para": 'n', "new_sent": "n"}
			else:
				edu_dict[edus_info[0]] = {"sent_id": sent_id, "new_sent": "y"}
				for edu in edus_info[1:]:
					edu_dict[edu] = {"sent_id": sent_id, "new_sent": "n"}

	return edu_dict


if __name__ == "__main__":
	# test case
	script_dir = os.getcwd()
	data_dir = script_dir.replace("utils", "data") + os.sep
	conllu_dir = data_dir + "conllu" + os.sep

	edu_info_dict = process_conllu(os.path.join(conllu_dir, "GUM_academic_discrimination.conllu"))
