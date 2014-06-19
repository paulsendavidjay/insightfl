from flask import render_template, request, g, Flask, make_response
from app import app, host, port, user, passwd, db
from app.helpers.database import con_db
from app.helpers.app_funcs import first_n_drugs_assoc_indic, first_n_effects, get_side_effect_probabilities, plot_single_effect
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os, mpld3, io

# To create a database connection, add the following
# within your view functions:
# con = con_db(host, port, user, passwd, db)

def get_db():
	'''Open new connection to db'''
	if not hasattr(g, 'mysql_db'):
		g.mysql_db = con_db(host='127.0.0.1',
			port=3306, user='root', db='RxFx_indic_birCntl_depr', passwd='')
	return g.mysql_db

@app.teardown_appcontext
def close_db(error):
		"""Closes the database again at the end of the request."""
		if hasattr(g, 'mysql_db'):
				g.mysql_db.close()


# ROUTING/VIEW FUNCTIONS
@app.route('/')
@app.route('/index')
def index():
		# Renders index.html.
		return render_template('index.html')
@app.route('/RxFx', methods=['GET', 'POST'])
def RxFx():
		# Renders RxFx.html.
		conn = get_db() 	# returns connection object
		c = conn.cursor() # create cursor object
		
		if request.method=='GET':
			# handle ask for informaion
			indication=""
			slider_dict = {}
			n_side_effects = 5
			side_effect_names=[]
			pref_list=n_side_effects*[0]
			recommendation = ""
			alternates = ""
			plot_html=""
		elif request.method=='POST':
			# handle processing information
			indication = request.form['indication']
			
			# ENTER ALGORITHM FUNCTION HERE
			n=request.form['n_side_effects']
			side_effect_names = first_n_effects(n, indication, conn)
			
			pref_list=[]
			# THIS IS JUST FOR KEEPING THE SAME VALUES
			for i in side_effect_names:
				try:
					pref_list.append(int(request.form[i]))
				except:
					pref_list.append(0)
			
			
			prob_df = get_side_effect_probabilities(tuple(side_effect_names), indication, conn)
			prob_table = pd.pivot_table(prob_df, 'effect_proportion', rows='side_effect', cols='medicinalproduct')
			prob_table = prob_table.fillna(0)
			
			dot_product = np.dot(pref_list, prob_table)
			medicinalproducts = list(prob_table.columns.values)
			score_df = pd.DataFrame(dot_product, index=medicinalproducts, columns=['score'])
			score_df=score_df.sort_index(by=['score'])
			recommendation = score_df.iloc[0].name
			alternates = score_df.index[1:4]
			
			
			plot_html = plot_single_effect(prob_table.iloc[:,0])
			
			
		return render_template('RxFx.html', 
			indication=indication,
			side_effect_names=side_effect_names,
			n_sliders=len(side_effect_names), 
			pref_list=pref_list,
			recommendation=recommendation,
			alternates=alternates,
			plot_html=plot_html)



@app.route('/drug_comparisons')
def drug_comparisons():
		# Renders slides.html.
		return render_template('drug_comparisons.html')

@app.route('/images/nanner')
def images(cropzonekey):
	return render_template("images.html", title=cropzonekey)

@app.route('/fig/<cropzonekey>')
def fig(cropzonekey):
	fig = plt.plot([0,1,2]
	img = io.StringIO()
	fig.savefig(img)
	img.seek(0)
	return send_file(img, mimetype='image/png')



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
