from flask import render_template, request, Flask, make_response, session, send_file, g
from app import app, host, port, user, passwd, db
from app.helpers.database import con_db
from app.helpers.app_funcs import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os, pickle
from StringIO import StringIO

app.secret_key = os.urandom(24)


# session['counter'] = 0

# To create a database connection, add the following
# within your view functions:
# con = con_db(host, port, user, passwd, db)


# PROVIDE A CONNECTION OBJECT ONLY IF ONE IS NOT ALREADY CONNECTED
def get_db():
	'''Open new connection to db'''
	if not hasattr(g, 'mysql_db'):
		g.mysql_db = con_db(host='127.0.0.1',
			port=3306, user='root', db='RxFx', passwd='')
	return g.mysql_db



@app.teardown_appcontext
def close_db(error):
		"""Closes the database again at the end of the request."""
		if hasattr(g, 'mysql_db'):
				g.mysql_db.close()





# ROUTING/VIEW FUNCTIONS
@app.route('/index')
def index():
		# Renders index.html.
		return render_template('index.html')



@app.route('/')
@app.route('/RxFx', methods=['GET', 'POST'])
def RxFx():
		# Renders RxFx.html.
		conn = get_db() 	# returns connection object
		c = conn.cursor() # create cursor object
		# GET LIST OF INDICATIONS
		query_string = '''
			SELECT indication, indication_single_term 
			FROM top_indications'''
		indication_list = pd.io.sql.frame_query(query_string, conn).sort("indication")
		indications = list(indication_list['indication'])
		indications_single_term = list(indication_list['indication_single_term'])
		
		if request.method=='GET':
			# handle ask for informaion
			indication=""
			slider_dict = {}
			n_side_effects = 5
			side_effect_names=[]
			pref_list=n_side_effects*[0]
			recommendation = ""
			alternates = ""
			single_plot_data_json=""
		elif request.method=='POST':
			# handle processing information
			indication = request.form['indication']
			
			#return indication
			
			# ENTER ALGORITHM FUNCTION HERE
			n=request.form['n_side_effects']
			
			# GET TOP SIDE EFFECTS ASSOCIATED WITH DRUG
			side_effect_names = first_n_effects(n, indications_dict[indication], conn)

			pref_list=[]
			# THIS IS JUST FOR KEEPING THE SAME VALUES
			for i in side_effect_names:
				try:
					pref_list.append(int(request.form[i]))
				except:
					pref_list.append(0)
			
			prob_df = get_side_effect_probabilities(tuple(side_effect_names), str(indications_dict[indication]), conn)
			prob_table = pd.pivot_table(prob_df, 'effect_proportion', rows='side_effect', cols='drug_short_name')
			prob_table = prob_table.fillna(0)
			
			print "RXFX: prob_table1", str(prob_table)
			
			dot_product = np.dot(pref_list, prob_table)
			drug_short_names = list(prob_table.columns.values)
			
			#print "drug_short_names:", str(drug_short_names)
			
			score_df = pd.DataFrame(dot_product, index=drug_short_names, columns=['score'])
			score_df=score_df.sort_index(by=['score'])
			recommendation = score_df.iloc[0].name
			alternates = score_df.index[1:4]
			
			#print "prob table2:", str(prob_table.iloc[:][recommendation])
			
			#g.single_plot_data = prob_table.iloc[:][recommendation]
			single_plot_data_json = pd.DataFrame(prob_table.iloc[:][recommendation]).to_json()
			print "RXFX: single_plot_data_json", str(single_plot_data_json)
			
		return render_template('RxFx.html', 
			indication=indication,
			side_effect_names=side_effect_names,
			n_effects=len(side_effect_names), 
			pref_list=pref_list,
			recommendation=recommendation,
			alternates=alternates,
			indications = indications,
			indications_single_term = indications_single_term,
			single_plot_data_json = single_plot_data_json
			)



# ROUTING/VIEW FUNCTIONS


@app.route('/single_effect_png/<data_string>', methods=['GET','POST'])
def single_effect_png(data_string):
	'''Expects pandas data slice of side effects and drug name'''	
	single_effect_plot_data = pd.read_json(data_string)
	t = open("tst.txt", 'a')
	t.write(str(data_string))
	t.write(str(single_effect_plot_data))
	t.close()
	
	print "SINGLE EFFECT PNG: single_effect_plot_data", single_effect_plot_data
	values = list(single_effect_plot_data.ix[:,0])
	indices = [x.encode('UTF8') for x in list(single_effect_plot_data.index)] 
	#print values, indices
	fig=plt.figure();
	#single_effect_plot_data.plot(kind='bar')
	plt.bar(range(0,len(indices)), values, align='center') # test plot
	plt.axhline(0, color='k')
	plt.xlabel('side effect', fontsize=16)
	plt.ylabel('proportion of reported cases', fontsize=16)
	plt.xticks(range(0,len(indices)), indices, rotation=45)
	plt.title("Occurence of Side Effects", color='black', fontsize=20)
	fig.autofmt_xdate(ha='right')
	
	img = StringIO()
	fig.savefig(img)
	img.seek(0)
	return send_file(img, mimetype='image/png')
 



@app.route('/drug_comparisons', methods=['GET', 'POST'])
def drug_comparisons():
		conn = get_db() 	# returns connection object
		c = conn.cursor() # create cursor object
		
		query_string = '''
			SELECT indication, indication_single_term 
			FROM top_indications'''
		indication_list = pd.io.sql.frame_query(query_string, conn).sort("indication")
		indications = list(indication_list['indication'])
		indications_single_term = list(indication_list['indication_single_term'])
		
		if request.method=='GET':
			query_string = '''
				SELECT drug_short_name
				FROM drugs_by_indication_short
				WHERE drugindication = "{0}"'''.format(indications[0])
			druglist = list(pd.io.sql.frame_query(query_string, conn).sort("drug_short_name").ix[:,0])
			
			current_indication=indications[0]
		elif request.method=='POST':
			current_indication = request.form['indication']
			query_string = '''
				SELECT drug_short_name
				FROM drugs_by_indication_short
				WHERE drugindication = "{0}"'''.format(current_indication)
			druglist = list(pd.io.sql.frame_query(query_string, conn).sort("drug_short_name").ix[:,0])
			
			
			
			#current_Rx_list = request.form['Rx']
			#print current_Rx_list
		
		print str(druglist)
		return render_template('drug_comparisons.html',
			indications = indications,
			indications_single_term = indications_single_term,
			druglist = druglist, current_indication = current_indication
			)

@app.route('/analytics')
def analytics():
		# Renders slides.html.
		return render_template('analytics.html')




@app.route('/slides')
def about():
		# Renders slides.html.
		return render_template('slides.html')

@app.route('/author')
def contact():
		# Renders author.html.
		return render_template('author.html')



@app.errorhandler(404)
def page_not_found(error):
		return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
		return render_template('500.html'), 500


if __name__=="__main__":
	app.run(host='0.0.0.0', port=5000)
