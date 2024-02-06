"""
This script aims to extract relevant and necessary information from RSTDT .rsd and .conllu files
in order to construct a table of facts for further analysis and modeling to study RST parsing errors
"""

import io
import os
from collections import Counter
from relation2class4rstdt import rel2class
from process_preds import bottom_up_pred_dict_RSTDT, top_down_pred_dict_RSTDT
from get_oov_rate import RSTDT_TEST_EDU_OOV_COUNT_DICT
from get_gold_anno import obtain_token_ids, process_conllu
from get_dep_info_rstdt import dep_direct_dict, edu_dep_dict


script_dir = os.getcwd()
data_dir = script_dir.replace("utils", "data") + os.sep + "RSTDT" + os.sep

# directories for rsd+dm files from GUM test+dev
human_dir = data_dir + "human" + os.sep


# other GUM anno file directories
conllu_dir = data_dir + "conllu" + os.sep

HEADER = f"doc_name\tgenre\tedu_id\tedu_txt\tCDU\tedu_len\tgold_rel_label\tgold_rel_class\tgold_inersent\t" \
         f"gold_child_count\tgold_descendant_count\tedu_oov_rate\t" \
         f"attach_error_top\tattach_error_bot\tattach_label_error_count_top\tattach_label_error_count_bot\t" \
         f"pred_rel_top_1\tpred_rel_top_2\tpred_rel_top_3\tpred_rel_top_4\tpred_rel_top_5\tpred_rel_top_majority\tpred_rel_top_majority_count\t" \
         f"pred_rel_bot_1\tpred_rel_bot_2\tpred_rel_bot_3\tpred_rel_bot_4\tpred_rel_bot_5\tpred_rel_bot_majority\tpred_rel_bot_majority_count\t" \
         f"dm\tdm_form\tdistractor\tdistractor_form\tdistractor_rel_label\tdistractor_rel_class"
table_lines = [HEADER]

for file in sorted(os.listdir(human_dir), key=lambda x: x.split("_")):
	if file.startswith("wsj"):
		filename = file.split(".")[0]
		genre = "WSJ"

		token_dict = obtain_token_ids(os.path.join(human_dir, file))
		doc_dict = process_conllu(os.path.join(conllu_dir, filename+".conllu"), GUM=False)

		gold_lines = io.open(os.path.join(human_dir, file), "r", encoding="utf-8").read().strip().split("\n")

		# initialize variables
		dm_form = ""
		distractor_form = ""
		distractor_rel_label = ""
		distractor_rel_class = ""
		gold_head_dep_func = ""
		distractor_form_individual = ""

		for idx, line in enumerate(gold_lines):
			gold_line = line.split("\t")

			edu_id = int(gold_line[0])
			edu_tt = gold_line[1].replace('"', "&quot;").replace("'", "&apos;")
			edu_len = int(len(edu_tt.split(" ")))

			# relation-related information: coarse, fine-grained, and CDU
			gold_rel_label = gold_line[7].split("_")[0]  # fine-grained
			if gold_rel_label == "ROOT":
				gold_rel_class = "root"
			else:
				gold_rel_class = rel2class[gold_rel_label].lower()  # coarse-grained, lowercase

			if gold_line[7] == "ROOT":
				CDU_FIELD = "y"
			else:
				CDU_FIELD = "n"

			# gold annotation feature information: g_intersent (between sents); g_interpara (between paras); g_adnominal
			g_intersent = doc_dict[edu_id]["new_sent"]

			# OOV rate for each EDU (% token forms in the EDU which are unattested in GUM train)
			oov_dict = RSTDT_TEST_EDU_OOV_COUNT_DICT[filename]
			oov_rate_per_edu = round(oov_dict[edu_id]["unattested_tok_count"] / oov_dict[edu_id]["edu_tok_count"], 4)

			# Number of dependency children in the gold graph (direct)
			dep_child_count_dict = dep_direct_dict[filename]
			if edu_id in dep_child_count_dict:
				direct_child_count = dep_child_count_dict[edu_id]
			else:
				direct_child_count = 0

			# Number of dependency descendants in the gold graph (indirect, i.e. recursive dependency count)
			dep_descendant_count_dict = edu_dep_dict[filename]
			dep_descendant_list_doc_level = []
			for edu_idx in dep_descendant_count_dict:
				dep_descendant_list = []
				temp = dep_descendant_count_dict[edu_idx]

				while temp != 0:
					dep_descendant_list.append(temp)
					temp = dep_descendant_count_dict[temp]

				# print(dep_descendant_list)
				if len(dep_descendant_list) == 2:
					dep_descendant_list_doc_level.append(dep_descendant_list[1])
				elif len(dep_descendant_list) > 2:
					dep_descendant_list_doc_level += dep_descendant_list[1:]

			indirect_child_count_dict = Counter(dep_descendant_list_doc_level)

			if edu_id in indirect_child_count_dict:
				descendant_count = indirect_child_count_dict[edu_id]
			else:
				descendant_count = 0

			# predicted relation classes - BOTTOM UP: majority
			pred_rel_bot_counter = Counter(bottom_up_pred_dict_RSTDT[filename][edu_id]["relclass"])
			most_predicted_rel_bot = [key for key, vale in pred_rel_bot_counter.items() if vale == max(pred_rel_bot_counter.values())]
			pred_rel_bot_majority = ";".join(most_predicted_rel_bot)
			pred_rel_bot_count = pred_rel_bot_counter[most_predicted_rel_bot[0]]

			# attachment-related information: BOTTOM UP
			gold_attachment = int(gold_line[6])
			attach_bot = bottom_up_pred_dict_RSTDT[filename][edu_id]["attachment"].count(0)

			# attachment error OR label error
			attachment_pred_bot = bottom_up_pred_dict_RSTDT[filename][edu_id]["attachment"]  # binary: 0 means incorrect; 1 means correct
			relation_pred_bot = bottom_up_pred_dict_RSTDT[filename][edu_id]["relclass"]
			assert len(attachment_pred_bot) == len(relation_pred_bot) == 5
			pred_rel_bot_1, pred_rel_bot_2, pred_rel_bot_3, pred_rel_bot_4, pred_rel_bot_5 = relation_pred_bot

			bottom_up_imperf_count = 0
			for item_idx, item in enumerate(attachment_pred_bot):
				if item == 0 or relation_pred_bot[item_idx] != gold_rel_class:
					bottom_up_imperf_count += 1

			# TOP DOWN
			# predicted relation classes - TOP DOWN: majority
			pred_rel_top_counter = Counter(top_down_pred_dict_RSTDT[filename][edu_id]["relclass"])
			most_predicted_rel_top = [key for key, vale in pred_rel_top_counter.items() if vale == max(pred_rel_top_counter.values())]
			pred_rel_top_majority = ";".join(most_predicted_rel_top)
			pred_rel_top_count = pred_rel_top_counter[most_predicted_rel_top[0]]

			# attachment-related information: TOP DOWN
			gold_attachment = int(gold_line[6])
			attach_top = top_down_pred_dict_RSTDT[filename][edu_id]["attachment"].count(0)

			# attachment error OR label error
			attachment_pred_top = top_down_pred_dict_RSTDT[filename][edu_id]["attachment"]  # binary: 0 means incorrect; 1 means correct
			relation_pred_top = top_down_pred_dict_RSTDT[filename][edu_id]["relclass"]
			assert len(attachment_pred_top) == len(relation_pred_top) == 5
			pred_rel_top_1, pred_rel_top_2, pred_rel_top_3, pred_rel_top_4, pred_rel_top_5 = relation_pred_top

			top_down_imperf_count = 0
			for item_idx, item in enumerate(attachment_pred_top):
				if item == 0 or relation_pred_top[item_idx] != gold_rel_class:
					top_down_imperf_count += 1

			# DM-related information
			signal_field = gold_line[9]  # e.g. dm-dm-963 OR dm-dm-556,557
			if "dm-dm" in signal_field:
				dm = "y"
				dm_token_ids = [item for item in signal_field.split(";") if item.startswith("dm-dm")]
				if len(dm_token_ids) == 1:  # ['dm-dm-774']
					token_id_field = dm_token_ids[0].split("-")[-1]
					if "," not in token_id_field:
						dm_form = token_dict[int(token_id_field)]
					else:
						tok_ids = [int(item) for item in token_id_field.split(",")]
						tok_ids = list(sorted(tok_ids))
						dm_form = " ".join([token_dict[int(tok_id)] for tok_id in tok_ids])
				else:  # e.g. ['dm-dm-691', 'dm-dm-692']
					dms = []
					for item in dm_token_ids:
						token_id_field = item.split("-")[-1]
						if "," not in token_id_field:
							dm_form_individual = token_dict[int(token_id_field)]
						else:
							dm_form_individual = " ".join([token_dict[int(tok_id)] for tok_id in token_id_field.split(",")])
						dms.append(dm_form_individual)
					dm_form = ";".join(dms)
			else:
				dm = "n"
				dm_form = "NA"

			# DM-orphan information
			orphan_signal_field = gold_line[8]  # 132:causal-result:4:3:orphan-orphan-1036
			if orphan_signal_field == "_":
				distractor = "n"
				distractor_form = "NA"
				distractor_rel_label = "NA"
				distractor_rel_class = "NA"
			elif "orphan-orphan-" not in orphan_signal_field:  # e.g. 122:attribution-positive:2:0:unsure-unsure-
				distractor = "n"
				distractor_form = "NA"
				distractor_rel_label = "NA"
				distractor_rel_class = "NA"
			else:
				distractor = "y"
				if "|" in orphan_signal_field:
					# 37:adversative-antithesis:0:0:_|36:causal-result:0:0:orphan-orphan-198
					# 66:adversative-concession:1:4:orphan-orphan-558|59:adversative-concession:1:3:orphan-orphan-536
					orphan_items = orphan_signal_field.split("|")
					distractors = []
					for item in orphan_items:
						if "orphan-orphan-" in item:
							distractor_rel_label = item.split(":")[1]
							distractor_rel_class = item.split(":")[1].split("-")[0]
							distractor_tokid = item.split("-")[-1]
							if "," not in distractor_tokid:
								distractors.append(token_dict[int(distractor_tokid)])
							else:
								distractor_tokid_list = distractor_tokid.split(",")
								distractor_form_individual = " ".join([token_dict[int(distactor_tokid)] for distactor_tokid in distractor_tokid_list])
							distractors.append(distractor_form_individual)
					distractor_form = ";".join(distractors)

				elif ";" in orphan_signal_field:
					orphan_items = orphan_signal_field.split(";")
					distractors = []
					if orphan_signal_field.count("orphan-orphan-") > 1:
						distractor_rel_label = orphan_items[0].split(":")[1]
						distractor_rel_class = orphan_items[0].split(":")[1].split("-")[0]
						distractor_tokid_1 = orphan_items[0].split("-")[-1]
						distractor_form_1 = token_dict[int(distractor_tokid_1)]
						distractors.append(distractor_form_1)
						distractor_tokid_2 = orphan_items[1].split("-")[-1]
						distractor_form_2 = token_dict[int(distractor_tokid_2)]
						distractors.append(distractor_form_2)
					else:
						for item in orphan_items:
							if "orphan-orphan-" in item:
								distractor_rel_label = item.split(":")[1]
								distractor_rel_class = item.split(":")[1].split("-")[0]
								distractor_tokid = item.split("-")[-1]
								distractor_form_individual = " ".join([token_dict[int(distractor_tokid)] for tokid in item.split(",")])
								distractors.append(distractor_form_individual)
					distractor_form = ";".join(distractors)

				else:
					distractor_rel_label = orphan_signal_field.split(":")[1]
					distractor_rel_class = orphan_signal_field.split(":")[1].split("-")[0]
					distractor_tokid = orphan_signal_field.split("-")[-1]
					distractor_form = " ".join([token_dict[int(orphan_id)] for orphan_id in distractor_tokid.split(",")])

			# line of facts
			out_line = f"{filename}\t{genre}\t{edu_id}\t{edu_tt}\t{CDU_FIELD}\t{edu_len}\t{gold_rel_label}\t{gold_rel_class}\t" \
			           f"{g_intersent}\t" \
			           f"{direct_child_count}\t{descendant_count}\t{oov_rate_per_edu}\t" \
			           f"{attach_top}\t{attach_bot}\t{top_down_imperf_count}\t{bottom_up_imperf_count}\t" \
			           f"{pred_rel_top_1}\t{pred_rel_top_2}\t{pred_rel_top_3}\t{pred_rel_top_4}\t{pred_rel_top_5}\t" \
			           f"{pred_rel_top_majority}\t{pred_rel_top_count}\t" \
			           f"{pred_rel_bot_1}\t{pred_rel_bot_2}\t{pred_rel_bot_3}\t{pred_rel_bot_4}\t{pred_rel_bot_5}\t" \
			           f"{pred_rel_bot_majority}\t{pred_rel_bot_count}\t" \
			           f"{dm}\t{dm_form}\t{distractor}\t{distractor_form}\t{distractor_rel_label}\t{distractor_rel_class}"

			table_lines.append(out_line)


# write to file
with open(os.path.join(data_dir, "RSTDT_facts.tab"), "w", encoding="utf-8") as f_out:
	f_out.write("\n".join(table_lines))
