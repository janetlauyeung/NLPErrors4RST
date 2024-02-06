import io
import os
from collections import defaultdict, Counter
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
from textwrap import wrap


def make_genre_dict(fact_data):

	genre_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

	for line in fact_data[1:]:  # excluding header
		fields = line.split("\t")
		genre = fields[2]

		# DM
		dm_field = fields[-6]
		if dm_field == "y":
			genre_dict[genre]["dm"]["y"] += 1
			genre_dict[genre]["gold_rel_class"]["dm_y"] += 1
		else:
			genre_dict[genre]["dm"]["n"] += 1
			genre_dict[genre]["gold_rel_class"]["dm_n"] += 1

		# attachment
		# attachment_top_error_count = int(fields[11])
		# attachment_bot_error_count = int(fields[12])
		# genre_dict[genre]["attach_top"][attachment_top_error_count] += 1
		# genre_dict[genre]["attach_bot"][attachment_bot_error_count] += 1

		# distractor-DM
		distractor = fields[-4]
		if distractor == "y":
			genre_dict[genre]["distractor"]["y"] += 1
		else:
			genre_dict[genre]["distractor"]["n"] += 1

	return genre_dict


def make_rel_dict(fact_data):
	rel_dict = defaultdict(lambda: defaultdict(int))

	for line in fact_data[1:]:  # excluding header
		fields = line.split("\t")
		gold_rel_class = fields[8]
		dm_field = fields[-6]
		if dm_field == "y":
			rel_dict[gold_rel_class]["explicit"] += 1
		else:
			rel_dict[gold_rel_class]["implicit"] += 1

	rel_dict = dict(sorted(rel_dict.items(), key=lambda x: x[0]))

	return rel_dict


if __name__ == "__main__":
	script_dir = os.getcwd()
	data_dir = script_dir.replace("utils", "data") + os.sep + "GUM9" + os.sep
	filename = "GUM_facts.tab"

	facts = io.open(os.path.join(data_dir, filename), "r", encoding="utf-8").read().strip().split("\n")
	total_instance_count = len(facts[1:])

	genre_dict = make_genre_dict(facts)
	attachment_error_regroup = defaultdict(lambda: defaultdict(dict))

	count = 0
	distractors = defaultdict(int)
	distractors_info_dict = defaultdict(lambda: defaultdict(list))
	for fact_line in facts[1:]:
		fact_line_fields = fact_line.split("\t")
		if fact_line_fields[-4] == "y" and fact_line_fields[8] not in fact_line_fields[-8]:  # fact_line_fields[8] != fact_line_fields[23]; fact_line_fields[20] != "0"
			count += 1

		distractor_forms = fact_line_fields[-3]
		subord_info = fact_line_fields[11]
		genre_info = fact_line_fields[2]
		if "NA" not in distractor_forms:
			if ";" not in distractor_forms:
				distractors[distractor_forms] += 1
				distractors_info_dict[distractor_forms]["subord"].append(subord_info)
				distractors_info_dict[distractor_forms]["genre"].append(genre_info)
			else:
				distractor_list = distractor_forms.split(";")
				for item in distractor_list:
					distractors[item] += 1
					distractors_info_dict[item]["subord"].append(subord_info)
					distractors_info_dict[item]["genre"].append(genre_info)

	distractors_sorted = dict(sorted(distractors.items(), key=lambda tup: tup[1], reverse=True))
	# for item in distractors_sorted:
	# 	print(item, "\t", distractors_sorted[item])

	distractor_genre_dict = defaultdict(int)
	for distractor_key in distractors_info_dict:
		subord_dict_counter = Counter(distractors_info_dict[distractor_key]["subord"])
		genre_dict_counter = Counter(distractors_info_dict[distractor_key]["genre"])
		print(distractor_key, "\t", subord_dict_counter["y"], "\t", subord_dict_counter["n"], '\t', [(key, genre_dict_counter[key]) for key in genre_dict_counter])
		genre_list = distractors_info_dict[distractor_key]["genre"]  # a list
		for genre in genre_list:
			distractor_genre_dict[genre] += 1
	distractor_genre_dict_sorted = dict(sorted(distractor_genre_dict.items(), key=lambda tup: tup[1], reverse=True))
	# for k in distractor_genre_dict_sorted:
	# 	print(k, "\t", distractor_genre_dict_sorted[k])

	# print(count)

	for genre_key in genre_dict:
		genre_sub_dict = genre_dict[genre_key]

		# extracting
		explicit_instance_count = genre_sub_dict['dm']['y']
		implicit_instance_count = genre_sub_dict['dm']['n']
		distractor_instance_count = genre_sub_dict['distractor']['y']

		# explicit / implicit / distractor counts
		rel_type_line = f"{genre_key}\t{explicit_instance_count}\t{implicit_instance_count}\t{distractor_instance_count}"
		# print(rel_type_line)

	# relation analysis
	rel_dict = make_rel_dict(facts)
	for rel_key in rel_dict:
		rel_sub_dict = rel_dict[rel_key]
		if "explicit" not in rel_sub_dict:
			rel_sub_dict["explicit"] = 0
		if "implicit" not in rel_sub_dict:
			rel_sub_dict["implicit"] = 0

		rel_class_line = f"{rel_key}\t{rel_sub_dict['explicit']}\t{rel_sub_dict['implicit']}"
		# print(rel_class_line)
