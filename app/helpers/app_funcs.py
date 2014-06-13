import pandas as pd


'''
THIS FUNCTION SELECTS THE TOP N DRUGS ASSOCIATED WITH AN INDICATION
'''
def first_n_drugs_assoc_indic(n, indication, conn):
	query_string = '''
		SELECT drg.medicinalproduct
		FROM drugs drg
		JOIN indications ind
		ON drg.drug_id = ind.drug_id
		WHERE ind.drugindication = '{0}'
		GROUP BY drg.medicinalproduct
		ORDER BY COUNT(drg.medicinalproduct) DESC
		LIMIT {1}'''.format(indication, n)
	result_df = pd.io.sql.frame_query(query_string, conn)
	result = tuple(result_df['medicinalproduct'])
	return result


'''
THIS FUNCTION SELECTS THE TOP N EFFECTS ASSOCIATED WITH AN INDICATION.
TOP N ARE SELECTED BY FIRST SORTING BY THE NUMBER OF SIDE EFFECTS ASSOCIATED
WITH THE DRUG, THEN BY THE SUM OF PROBABILITIES ACROSS DRUGS. 
'''
def first_n_effects(n, indication, conn):
	query_string = '''
		SELECT side_effect, COUNT(side_effect) AS tot_effect_count, SUM(effect_proportion)
		FROM {0}_effect_props
		WHERE side_effect NOT IN ("DRUG INEFFECTIVE", "COMPLETED SUICIDE", "DRUG INTERACTION", "DEPRESSION")
		GROUP BY side_effect
		ORDER BY tot_effect_count DESC, SUM(effect_proportion) DESC
		LIMIT {1}'''.format(indication, n)
	result_df = pd.io.sql.frame_query(query_string, conn)
	result = list(result_df['side_effect'])
	return result


def get_side_effect_probabilities(side_effect_tuple, indication, conn):
	query_string = '''
		SELECT side_effect, medicinalproduct, effect_proportion
		FROM {0}_effect_props
		WHERE side_effect IN {1}'''.format(indication, side_effect_tuple)
	result_df = pd.io.sql.frame_query(query_string, conn)
	return result_df
	


