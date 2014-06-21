import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from StringIO import StringIO
import pickle

indications_dict = pickle.load( open( "app/helpers/indications_dict.p", "rb" ) )


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


def get_side_effect_probabilities(side_effect_tuple, indication_single_term, conn):
	query_string = '''
		SELECT side_effect, drug_short_name, SUM(side_effect_count/patient_count) AS effect_proportion
		FROM {0}_props
		WHERE side_effect IN {1}
		GROUP BY side_effect, drug_short_name'''.format(indication_single_term, side_effect_tuple)
	result_df = pd.io.sql.frame_query(query_string, conn)
	return result_df
	


def get_side_effect_probs_by_single_drug(side_effect_tuple, indication_single_term, drug, conn):
	query_string = '''
		SELECT side_effect, SUM(side_effect_count/patient_count) AS effect_proportion
		FROM {0}_props
		WHERE side_effect IN {1}
		AND drug_short_name = "{2}"
		GROUP BY side_effect, drug_short_name'''.format(indication_single_term, side_effect_tuple, drug)
	result_df = pd.io.sql.frame_query(query_string, conn)
	return result_df







def plot_single_effect(pd_slice):
	'''Expects pandas data slice of side effects and drug name'''
	fig=plt.figure();
	pd_slice.plot(kind='bar')
	plt.axhline(0, color='k')
	plt.xlabel('side effect')
	plt.ylabel('proportion of reported cases')
	plt.xticks(rotation=45)
	plt.title(pd_slice.name, color='black')
	fig.autofmt_xdate(rotation=45, ha='right')
	img = StringIO()
	fig.savefig(img)
	img.seek(0)
	return img


