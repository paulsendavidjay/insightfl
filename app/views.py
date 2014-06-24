from flask import render_template, request, Flask, make_response, session, send_file, g
from app import app, host, port, user, passwd, db
from app.helpers.database import con_db
from app.helpers.app_funcs import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ggplot import *
import os, pickle, ast
from StringIO import StringIO
import socket

app.secret_key = os.urandom(24)



# PROVIDE A CONNECTION OBJECT ONLY IF ONE IS NOT ALREADY CONNECTED
def get_db():
	'''Open new connection to db'''
	if not hasattr(g, 'mysql_db'):
		g.mysql_db = con_db(host=app.config["DATABASE_HOST"],
			port=app.config["DATABASE_PORT"], user=app.config["DATABASE_USER"], db=app.config["DATABASE_DB"], passwd=app.config["DATABASE_PASSWORD"])
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
			
			
			
			prob_df = get_side_effect_probabilities(str(indications_dict[indication]), tuple(side_effect_names), conn)
			prob_table = pd.pivot_table(prob_df, 'effect_proportion', rows='side_effect', cols='drug_short_name')
			prob_table = prob_table.fillna(0)
			
			dot_product = np.dot(pref_list, prob_table)
			drug_short_names = list(prob_table.columns.values)
			
			score_df = pd.DataFrame(dot_product, index=drug_short_names, columns=['score'])
			score_df=score_df.sort_index(by=['score'])
			recommendation = score_df.iloc[0].name
			alternates = score_df.index[1:4]
			
			single_plot_data_json = pd.DataFrame(prob_table.iloc[:][recommendation]).to_json()
			
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
	drug_name = str(single_effect_plot_data.columns.values[0])
	single_effect_plot_data=single_effect_plot_data.sort(drug_name, ascending=False)
	
	print "SINGLE EFFECT PNG: single_effect_plot_data", drug_name
	values = list(single_effect_plot_data.ix[:,0])
	indices = [x.encode('UTF8') for x in list(single_effect_plot_data.index)] 
	#print values, indices
	fig=plt.figure();
	#single_effect_plot_data.plot(kind='bar')
	plt.bar(range(0,len(indices)), values, align='center', color='blue') # test plot
	plt.axhline(0, color='k')
	plt.ylabel('proportion of reported cases', fontsize=16)
	plt.xticks(range(0,len(indices)), indices, rotation=45)
	plt.title(drug_name, color='black', fontsize=20)
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
		druglist=""
		if request.method=='GET':
			query_string = '''
				SELECT drug_short_name
				FROM drugs_by_indication_short
				WHERE drugindication = "{0}"'''.format(indications[0])
			druglist = list(pd.io.sql.frame_query(query_string, conn).sort("drug_short_name").ix[:,0])
			
			current_indication=indications[0]
			drug_selection=[]
		
		elif request.method=='POST':
			druglist=""
			current_indication = request.form['indication']
			query_string = '''
			SELECT drug_short_name
			FROM drugs_by_indication_short
			WHERE drugindication = "{0}"'''.format(current_indication)
			druglist = list(pd.io.sql.frame_query(query_string, conn).sort("drug_short_name").ix[:,0])
			 
			drug_selection = request.form.getlist('drugs_selected') 
			drug_selection = [x.encode('UTF8') for x in drug_selection]
			
			#current_Rx_list = request.form['Rx']
			#print current_Rx_list
		
		print drug_selection
		return render_template('drug_comparisons.html',
			indications = indications,
			indications_single_term = indications_single_term,
			druglist = druglist, 
			current_indication = current_indication,
			drug_selection = drug_selection
			)







@app.route('/multi_effect_png/<current_indication>/<drug_selection>', methods=['GET','POST'])
def multi_effect_png(current_indication, drug_selection):
	'''Expects pandas data slice of side effects and drug name'''	
	conn = get_db() 	# returns connection object
	
	drug_selection = ast.literal_eval(drug_selection)
	
	prob_df = get_side_effect_probs_for_multi_drug(current_indication, tuple(drug_selection), conn)
	
	prob_table = pd.pivot_table(prob_df, 'effect_proportion', rows='side_effect', cols='drug_short_name')
	prob_table = prob_table.fillna(0.00001)
	prob_df2 = prob_table.stack().reset_index()
	prob_df2.columns=['side_effect','drug','probability']
	
	col_names = ["","",""]#prob_table.columns.values
	ylimit = max(prob_df2['probability']+0.01)
	break_list = list(np.arange(len(col_names)) + 1)
	try:
		p = ggplot(prob_df2, aes(x='drug',weight='probability',fill="drug")) + \
			geom_bar() + \
			ylab("") + \
			xlab("") + \
			ylim(0,ylimit) +\
			scale_x_continuous(breaks=break_list,labels=list(col_names)) +\
			facet_wrap('side_effect', ncol=2)
		
		
		img2 = StringIO()
		fig=p.draw()
	except RuntimeWarning:
		pass	
	fig.set_size_inches(6,10.5)
	fig.savefig(img2, dpi=100)
	ggsave(plot=p, filename="test.png")	
	img2.seek(0)
	return send_file(img2, mimetype='image/png')









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
