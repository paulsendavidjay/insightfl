import pandas as pd

def first_n_main(n, indication, conn):
	if (indication == 'birth_control'):
		field = 'country'
	elif (indication == 'depression'):
		field = 'safetyreportid'
	
	query_string = '''
		SELECT DISTINCT {0} 
		FROM main 
		ORDER BY {0}
		LIMIT {1}'''.format(field, n)
	result_df = pd.io.sql.frame_query(query_string, conn)
	#temp = c.execute(query_string)
	#c.execute(query_string)
	#country = c.fetchone()[0]
	result = list(result_df[field])
	return result


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



# def first_n_effects(n, str_drug_list, conn):
# 	query_string = '''
# 		SELECT side.side_effect
# 		FROM (
# 			SELECT drg0.medicinalproduct, pat_drg0.patientid
# 			FROM drugs drg0
# 			JOIN patient_drugs pat_drg0
# 			ON drg0.drug_id = pat_drg0.drug_id
# 			WHERE drg0.medicinalproduct IN 
# 				{0}
# 				) AS drg
# 			JOIN patient_side_effects pat_side
# 				ON drg.patientid = pat_side.patientid
# 			JOIN side_effects side
# 				ON pat_side.side_effect_id = side.side_effect_id
# 			GROUP BY side.side_effect
# 			ORDER BY COUNT(drg.medicinalproduct) DESC, side.side_effect
# 			LIMIT {1}'''.format(str_drug_list, n)
# 	
# 	result_df = pd.io.sql.frame_query(query_string, conn)
# 	result = list(result_df['side_effect'])
# 	return result


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

