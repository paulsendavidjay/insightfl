import pandas as pd
import pymysql
import sys
import matplotlib.pyplot as plt


# Returns MySQL database connection
def con_db(host, port, user, passwd, db):
    try:
        con = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db)
    except pymysql.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    return con

def get_side_effect_probabilities(side_effect_tuple, indication, conn):
	query_string = '''
		SELECT side_effect, medicinalproduct, effect_proportion
		FROM {0}_effect_props
		WHERE side_effect IN {1}'''.format(indication, side_effect_tuple)
	result_df = pd.io.sql.read_sql(query_string, conn)
	return result_df



con = con_db(host='127.0.0.1',
			port=3306, user='root', db='RxFx_indic_birCntl_depr', passwd='')



prob_df = get_side_effect_probabilities(tuple(["NAUSEA","PAIN",'HEADACHE']), "CONTRACEPTION", con)
prob_table = pd.pivot_table(prob_df, 'effect_proportion', index='side_effect', columns='medicinalproduct')
prob_table = prob_table.fillna(0)
prob_table


