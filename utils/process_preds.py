"""
This script aims to process automatic parses from both parsers of 5 runs in order to obtain relevant information:
- number of times that a model gets the attachment wrong
- predicted relation labels and relation classes

"""

import io
import os
from collections import defaultdict, Counter


script_dir = os.getcwd()
data_dir = script_dir.replace("utils", "data") + os.sep + "GUM9" + os.sep

# directories for rsd files from GUM test (gold or pred)
human_dir = data_dir + "human" + os.sep
top_down_dir = data_dir + "topdown" + os.sep
bottom_up_dir = data_dir + "bottomup" + os.sep


def extract(model_pred_dir, GUM=True):
	pred_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
	for sub_dir in os.listdir(model_pred_dir):
		if sub_dir.startswith("run"):
			for file in os.listdir(os.path.join(model_pred_dir, sub_dir)):
				if file.endswith(".rsd"):
					filename = file.split(".")[0]
					single_run_rsd_lines = io.open(os.path.join(os.path.join(model_pred_dir, sub_dir), file), "r", encoding="utf-8").read().strip().split("\n")
					if GUM is True:
						gold_rsd_lines = io.open(os.path.join(human_dir, file), "r", encoding="utf-8").read().strip().split("\n")
					else:
						gold_rsd_lines = io.open(os.path.join(human_dir.replace("GUM9", "RSTDT"), file), "r", encoding="utf-8").read().strip().split("\n")
					assert len(single_run_rsd_lines) == len(gold_rsd_lines)

					for idx, line in enumerate(gold_rsd_lines):
						gold_line_fields = line.split("\t")
						pred_line_fields = single_run_rsd_lines[idx].split("\t")

						edu_id = int(gold_line_fields[0])

						# attachment information
						gold_attachment = int(gold_line_fields[6])
						pred_attachment = int(pred_line_fields[6])
						if gold_attachment == pred_attachment:
							pred_dict[filename][edu_id]["attachment"].append(1)
						else:
							pred_dict[filename][edu_id]["attachment"].append(0)
						pred_dict[filename][edu_id]["gold_attachment"] = gold_attachment
						pred_dict[filename][edu_id]["pred_attachment"].append(pred_attachment)

						# relation class information
						pred_rel_class = pred_line_fields[7].lower().split("_")[0]  # lowercase relation class name for consistency
						pred_dict[filename][edu_id]["relclass"].append(pred_rel_class)

	if GUM is True:
		assert len(pred_dict) == 48, f"incorrect number of documents processed"
	else:
		assert len(pred_dict) == 38, f"incorrect number of documents processed"

	pred_dict = dict(sorted(pred_dict.items(), key=lambda item: item[0]))

	return pred_dict


# top_down_pred_dict = extract(top_down_dir)
# bottom_up_pred_dict = extract(bottom_up_dir)

bottom_up_pred_dict_RSTDT = extract(data_dir.replace("GUM9", "RSTDT") +"bottomup" + os.sep, GUM=False)
top_down_pred_dict_RSTDT = extract(data_dir.replace("GUM9", "RSTDT") +"topdown" + os.sep, GUM=False)


def toy_example_test(dict1, dict2):
	dict1 = extract(top_down_dir)
	dict2 = extract(bottom_up_dir)

	test_case = dict2["GUM_academic_discrimination"][74]["relclass"]
	test_case_counter = Counter(test_case)

	# get most predicted relation classes along with its count: could be more than one
	most_predicted_rel = [key for key, vale in test_case_counter.items() if vale == max(test_case_counter.values())]
	# print(";".join(most_predicted_rel))


if __name__ == "__main__":
	d1 = {}
	d2 = {}
	toy_example_test(d1, d2)
