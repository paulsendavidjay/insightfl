from flask import render_template, request, Flask, make_response, session, send_file
from app import app, host, port, user, passwd, db
from app.helpers.database import con_db
from app.helpers.app_funcs import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from StringIO import StringIO
import pickle 
import os, pickle, ast, json, urllib, socket

indications_dict = pickle.load( open( "app/helpers/indications_dict.p", "rb" ) )

app.secret_key = os.urandom(24)

conn = con_db(host=app.config["DATABASE_HOST"],
			port=app.config["DATABASE_PORT"], 
			user=app.config["DATABASE_USER"], 
			db=app.config["DATABASE_DB"], 
			passwd=app.config["DATABASE_PASSWORD"])


@app.route('/testing', methods=['GET','POST'])
def testing():
		# Renders testing.html.
		ranked_side_effect_list=request.json
		print ranked_side_effect_list["list"]
		print session['indication']
		return "one"


# ROUTING/VIEW FUNCTIONS

@app.route('/')
@app.route('/RxFx', methods=['GET','POST'])
def RxFx():
		# Renders RxFx.html.
		indication = ''
		
		# GET LIST OF INDICATIONS
		query_string = '''
			SELECT indication, indication_single_term 
			FROM top_indications'''
		indication_list = pd.io.sql.frame_query(query_string, conn).sort('indication')
		indications = list(indication_list['indication'])
		
		if request.method=='GET':
			return render_template('RxFx.html', 
				indication="ANXIETY",
				indications = indications)
		
		elif request.method=='POST':
			# HANDLE PROCESSING INFORMATION
			session['indication'] = request.form['indication']
			side_effect_names = first_n_effects(15, indications_dict[session['indication']], conn)
			return render_template('RxFx_effect_fields.html', 
				indication=session['indication'],
				indications = indications,
				side_effect_names=side_effect_names)			

		return render_template('RxFx_effect_fields.html', 
			indication=session['indication'],
			indications = indications,
			side_effect_names=side_effect_names)


@app.route('/RxFx_effect_fields', methods=['GET', 'POST'])
def RxFx_effect_fields(indication,indications):
	# Renders RxFx_effect_fields.html.
	if request.method=='GET':
		
		# GET TOP SIDE EFFECTS ASSOCIATED WITH INDICATION
		side_effect_names = first_n_effects(15, indications_dict["ANXIETY"], conn)
		side_effect_names = ["nuts"]

		return render_template('RxFx_effect_fields.html',
			side_effect_names=side_effect_names)
	
	elif request.method=='POST':
		
		# GET TOP SIDE EFFECTS ASSOCIATED WITH DRUG
		side_effect_names = first_n_effects(15, indications_dict[indication], conn)

		prob_df = get_side_effect_probabilities(str(indication), tuple(side_effect_names), conn)
		prob_table = pd.pivot_table(prob_df, 'effect_proportion', rows='side_effect', cols='drug_short_name')
		prob_table = prob_table.fillna(0)
		
		dot_product = np.dot(pref_list, prob_table)
		drug_short_names = list(prob_table.columns.values)
		
		score_df = pd.DataFrame(dot_product, index=drug_short_names, columns=['score'])
		score_df=score_df.sort_index(by=['score'])
		recommendation = score_df.iloc[0].name
		alternates = score_df.index[1:4]
		
	return render_template('RxFx_effect_fields.html',
		indication=indication,
		indications=indications,
		side_effect_names=side_effect_names)



@app.route('/RxFx_effectiveness', methods=['GET','POST'])
def RxFx_effectiveness():
		# Renders RxFx.html.
		indication = ''
		
		# GET LIST OF INDICATIONS
		query_string = '''
			SELECT indication, indication_single_term 
			FROM top_indications'''
		indication_list = pd.io.sql.frame_query(query_string, conn).sort('indication')
		indications = list(indication_list['indication'])
		indication_single_term = ""

		if request.method=='GET':
			return render_template('RxFx_effectiveness.html', 
				indication="ANXIETY",
				indications=indications,
				indication_single_term=indication_single_term)
		
		elif request.method=='POST':
			# HANDLE PROCESSING INFORMATION
			indication = request.form['indication']
			indication_single_term = str(indications_dict[indication])
			file_name = "images/" + indication_single_term + ".jpg"
			app.test_request_context()

			print file_name
			return render_template('RxFx_effectiveness.html', 
				indication=indication,
				indications=indications,
				indication_single_term=indication_single_term)			

		return render_template('RxFx_effectiveness.html', 
			indication=indication,
			indications=indications,
			indication_single_term=indication_single_term)








@app.route('/RxFx_recommendation', methods=['GET', 'POST'])
def RxFx_recommendation():
	# Returns recommdation list to j.query
	indication = urllib.unquote(request.args.get('indication'))
	indication = indication.encode('UTF8')
	try:
		ranked_side_effect_list_json=request.json
		ranked_side_effect_list = [x.encode('UTF8') for x in ranked_side_effect_list_json["list"]]
		ranks = range(1, len(ranked_side_effect_list)+1)
		ranks = [1.0/x for x in ranks]
		
		# GET PROBABILITIES OF SIDE EFFECTS
		prob_df = get_side_effect_probabilities(str(indications_dict[indication]), tuple(ranked_side_effect_list), conn)
		prob_table = pd.pivot_table(prob_df, 'effect_proportion', rows='side_effect', cols='drug_short_name')
		prob_table = prob_table.fillna(0)
		
		# GET SUM OF WEIGHTS X PROBABILITIES
		dot_product = np.dot(ranks, prob_table)
		drug_short_names = list(prob_table.columns.values)

		score_df = pd.DataFrame(dot_product, index=drug_short_names, columns=['score'])
		score_df=score_df.sort_index(by=['score'])
		recommendations = list(score_df.index)
		rec_json = json.dumps(recommendations)
	except:
		import sys
		etype, value, tb = sys.exc_info()
		import traceback
		return '<br>\n'.join(traceback.format_exception(etype, value, tb))
	return rec_json	



@app.route('/multi_effect_probs', methods=['GET','POST'])
def multi_effect_probs():
	# Gets probabilities of side effects for different drugs
	indication = urllib.unquote(request.args.get('indication'))
	indication = indication.encode('UTF8')
	data_list_json=request.json

	# CONVERT FROM UNICODE
	ranked_side_effect_list = [x.encode('UTF8') for x in data_list_json["rankedSideEffects"]]
	drug_list = [x.encode('UTF8') for x in data_list_json["drugList"]]	
	
	# REMOVE RANKED ITEMS THAT DON'T APPEAR IN INDEX LIST
	prob_df = get_side_effect_probs_for_multi_drug(str(indications_dict[indication]), tuple(drug_list), tuple(ranked_side_effect_list), conn)
	ranked_side_effect_list_copy = list(ranked_side_effect_list)
	indexSet = set(prob_df.loc[:]["side_effect"])
	for i in ranked_side_effect_list_copy:
		if i not in indexSet: 
			ranked_side_effect_list.remove(i)

	# MANIPULATE TO GET VALUES FOR ALL DRUGS, ALL SIDE EFFECTS
	prob_table = pd.pivot_table(prob_df, 'effect_proportion', rows='side_effect', cols='drug_short_name')
	prob_table = prob_table.fillna(0)
	prob_table = prob_table*100

	# SELECT SIDE EFFECTS IN RANKED SIDE EFFECT LIST, ROUND, AND CONVERT TO STR
	prob_table2 = prob_table.loc[ranked_side_effect_list,drug_list]
	prob_table2 = np.round(prob_table2, decimals=1)
	prob_table2 = prob_table2.astype(str)


	# RESET INDEX TO PUT SIDE EFFECTS IN MATRIX WITH PROBABILITIES
	prob_table3 = prob_table2.reset_index()

	#BUILD ARRAY OF ARRAYS
	header = list(prob_table2.columns.values)
	header[:0]=["SIDE EFFECT"]
	table_list = [header]
	for i in range(len(prob_table3)):
	    table_list.append(list(prob_table3.ix[i][:]))

	table_json = json.dumps(table_list)
	return table_json





@app.route('/static/images/<indication_single_term>.jpg', methods=['POST'])
def effectiveness_png():
	# DISPLAYS EFFECTIVENESS PROBABILITIES
	return 




@app.route('/slides')
def about():
		# Renders slides.html.
		return render_template('slides.html')

@app.route('/about')
def contact():
		# Renders author.html.
		return render_template('about.html')



@app.errorhandler(404)
def page_not_found(error):
		return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
		return render_template('500.html'), 500


if __name__=="__main__":
	app.run(host='0.0.0.0', port=5000)
