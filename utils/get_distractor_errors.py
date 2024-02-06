import os
import io
from collections import defaultdict, Counter


script_dir = os.getcwd()
data_dir = script_dir.replace("utils", "data") + os.sep


def retrieve_cases(tab_file: str):
	if tab_file.startswith("GUM"):
		file_path = os.path.join(data_dir+"GUM9", tab_file)
	else:
		file_path = os.path.join(data_dir + "RSTDT", tab_file)

	top_distractor_errors = []
	bot_distractor_errors = []

	facts = io.open(file_path, "r", encoding="utf-8").read().strip().split("\n")[1:]
	for idx, line in enumerate(facts):
		if "\t" in line:
			fields = line.split("\t")

			line_idx = idx+1
			edu_id = fields[3]
			gold_rel_class = fields[8]

			pred_rel_bot_majority = fields[-8]
			pred_rel_top_majority = fields[-15]

			distractor_status = fields[-4]
			distractor_forms = fields[-3]

			if distractor_status == "y" and pred_rel_bot_majority != gold_rel_class:
				out_line = f'{line_idx}\t{gold_rel_class}\t{pred_rel_bot_majority}\t{distractor_forms}'
				bot_distractor_errors.append(out_line)

			if distractor_status == "y" and pred_rel_top_majority != gold_rel_class:
				out_line = f'{line_idx}\t{gold_rel_class}\t{pred_rel_top_majority}\t{distractor_forms}'
				top_distractor_errors.append(out_line)

	return top_distractor_errors, bot_distractor_errors


if __name__ == "__main__":
	top_distractor_errors, bot_distractor_errors = retrieve_cases("GUM_facts.tab")
	print(len(bot_distractor_errors))
	for item in bot_distractor_errors:
		print(item)

	# print(len(top_distractor_errors))
	# for item in top_distractor_errors:
	# 	print(item)
