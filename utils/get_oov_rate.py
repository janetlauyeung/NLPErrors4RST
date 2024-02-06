"""
OOV rate for each EDU (% token forms in the EDU which are unattested in GUM train)
"""


import os
import io
from collections import defaultdict


script_dir = os.getcwd()
data_dir_GUM = script_dir.replace("utils", "data") + os.sep + "GUM9" + os.sep
data_dir_RSTDT = data_dir_GUM.replace("GUM9", "RSTDT")

# directories for rsd files from GUM test and train
human_dir_GUM = data_dir_GUM + "human" + os.sep
human_dir_RSTDT = data_dir_RSTDT + "human" + os.sep
GUM_TRAIN_PATH = data_dir_GUM + "GUM9TRAIN" + os.sep
RSTDT_TRAIN_PATH = data_dir_RSTDT + "RSTDTTRAIN" + os.sep

# initialize dicts
# GUM
GUM_TRAIN_TOKEN_DICT = defaultdict(int)
GUM_TEST_EDU_OOV_COUNT_DICT = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

# GUM
# TRAIN (.rsd)
for file in os.listdir(GUM_TRAIN_PATH):
	if file.startswith("GUM"):
		filename = file.split(".")[0]
		lines = io.open(os.path.join(GUM_TRAIN_PATH, file), "r", encoding="utf-8").read().strip().split("\n")
		for line in lines:
			if "\t" in line:
				fields = line.split("\t")
				edu_idx = int(fields[0])
				edu_txt = fields[1]
				edu_tok = edu_txt.split(" ")
				for tok in edu_tok:
					GUM_TRAIN_TOKEN_DICT[tok] += 1


# TEST (.rsd)
for file in os.listdir(human_dir_GUM):
	if file.startswith("GUM"):
		filename = file.split(".")[0]
		lines = io.open(os.path.join(human_dir_GUM, file), "r", encoding="utf-8").read().strip().split("\n")
		for line in lines:
			if "\t" in line:
				fields = line.split("\t")
				edu_idx = int(fields[0])
				edu_txt = fields[1]
				edu_tok = edu_txt.split(" ")
				GUM_TEST_EDU_OOV_COUNT_DICT[filename][edu_idx]["edu_tok_count"] = len(edu_tok)
				for tok in edu_tok:
					if tok not in GUM_TRAIN_TOKEN_DICT:
						GUM_TEST_EDU_OOV_COUNT_DICT[filename][edu_idx]["unattested_tok_count"] += 1

# print(GUM_TEST_EDU_OOV_COUNT_DICT["GUM_academic_discrimination"])


# RSTDT
RSTDT_TRAIN_TOKEN_DICT = defaultdict(int)
RSTDT_TEST_EDU_OOV_COUNT_DICT = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

# TRAIN (.rsd)
for file in os.listdir(RSTDT_TRAIN_PATH):
	if file.startswith("wsj"):
		filename = file.split(".")[0]
		lines = io.open(os.path.join(RSTDT_TRAIN_PATH, file), "r", encoding="utf-8").read().strip().split("\n")
		for line in lines:
			if "\t" in line:
				fields = line.split("\t")
				edu_idx = int(fields[0])
				edu_txt = fields[1]
				edu_tok = edu_txt.split(" ")
				for tok in edu_tok:
					RSTDT_TRAIN_TOKEN_DICT[tok] += 1


# TEST (.rsd)
for file in os.listdir(human_dir_RSTDT):
	if file.startswith("wsj"):
		filename = file.split(".")[0]
		lines = io.open(os.path.join(human_dir_RSTDT, file), "r", encoding="utf-8").read().strip().split("\n")
		for line in lines:
			if "\t" in line:
				fields = line.split("\t")
				edu_idx = int(fields[0])
				edu_txt = fields[1]
				edu_tok = edu_txt.split(" ")
				RSTDT_TEST_EDU_OOV_COUNT_DICT[filename][edu_idx]["edu_tok_count"] = len(edu_tok)
				for tok in edu_tok:
					if tok not in RSTDT_TRAIN_TOKEN_DICT:
						RSTDT_TEST_EDU_OOV_COUNT_DICT[filename][edu_idx]["unattested_tok_count"] += 1
