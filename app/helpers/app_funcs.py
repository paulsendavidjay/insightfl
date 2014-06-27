import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from StringIO import StringIO


'''
THIS FUNCTION GETS THE TOP INDICATIONS TABLE
'''
def get_top_indications(conn):
	query_string='''
		SELECT indication, indication_single_term
		FROM top_indications'''
	result_df = pd.io.sql.frame_query(query_string, conn)
	return result_df



'''
THIS FUNCTION SELECTS THE TOP N DRUGS ASSOCIATED WITH AN INDICATION
'''
def first_n_drugs_assoc_indic(n, indication, conn):
	query_string = '''
		SELECT drg.drug_short_name
		FROM drugs_short drg
		JOIN indications ind
		ON drg.drug_id = ind.drug_id
		WHERE ind.drugindication = '{0}'
		GROUP BY drg.drug_short_name
		ORDER BY COUNT(drg.drug_short_name) DESC
		LIMIT {1}'''.format(indication, n)
	result_df = pd.io.sql.frame_query(query_string, conn)
	result = tuple(result_df['drug_short_name'])
	return result


'''
THIS FUNCTION SELECTS THE TOP N EFFECTS ASSOCIATED WITH AN INDICATION.
TOP N ARE SELECTED BY FIRST SORTING BY THE NUMBER OF SIDE EFFECTS ASSOCIATED
WITH THE DRUG, THEN BY THE SUM OF PROBABILITIES ACROSS DRUGS. 
'''
def first_n_effects(n, indication_single_term, conn):
	query_string = '''
		SELECT side_effect, COUNT(side_effect) AS tot_effect_count, SUM(side_effect_count/patient_count) AS sum_effect_proportion
		FROM {0}_props
		WHERE side_effect NOT IN ("DRUG INEFFECTIVE", "COMPLETED SUICIDE", "DRUG INTERACTION", "DEPRESSION")
		GROUP BY side_effect
		ORDER BY tot_effect_count DESC, sum_effect_proportion DESC
		LIMIT {1}'''.format(indication_single_term, n)
	result_df = pd.io.sql.frame_query(query_string, conn)
	result = list(result_df['side_effect'])
	return result


def get_side_effect_probabilities(indication_single_term, side_effect_tuple, conn):
	query_string = '''
		SELECT side_effect, drug_short_name, (side_effect_count/patient_count) AS effect_proportion
		FROM {0}_props
		WHERE side_effect IN {1}
		GROUP BY side_effect, drug_short_name'''.format(indication_single_term, side_effect_tuple)
	result_df = pd.io.sql.frame_query(query_string, conn)
	return result_df
	


def get_side_effect_probs_for_single_drug(indication_single_term, drug_short_name, conn):
	query_string = '''
		SELECT drug_short_name, side_effect, (side_effect_count/patient_count) AS effect_proportion
		FROM {0}_props
		WHERE drug_short_name = "{1}"
		GROUP BY side_effect
		ORDER BY effect_proportion DESC
		LIMIT 10'''.format(indication_single_term, drug_short_name)
	result_df = pd.io.sql.frame_query(query_string, conn)
	return result_df




def get_side_effect_probs_for_multi_drug(indication_single_term, drug_tuple, conn):
	result_df = pd.DataFrame()
	for drug_short_name in drug_tuple:
		current_drug_effects = get_side_effect_probs_for_single_drug(indication_single_term, drug_short_name, conn)
		result_df = result_df.append(current_drug_effects)
	return result_df



