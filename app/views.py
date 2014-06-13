from flask import render_template, request, g
from app import app, host, port, user, passwd, db
from app.helpers.database import con_db
from app.helpers.app_funcs import first_n_drugs_assoc_indic, first_n_effects, get_side_effect_probabilities
import pandas as pd
import numpy as np

# To create a database connection, add the following
# within your view functions:
# con = con_db(host, port, user, passwd, db)

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
			recommendation = ""
		elif request.method=='POST':
			# handle processing information
			indication = request.form['indication']
			
			# ENTER ALGORITHM FUNCTION HERE
			n=request.form['n_side_effects']
			#return str(int(n).__class__.__name__)
			slider_names = first_n_effects(n, indication, conn)
			
			slider_dict={} # create empty dictionary for slider info
			pref_table=[]
			# THIS IS JUST FOR KEEPING THE SAME VALUES
			for key in slider_names:
				try:
					slider_dict[key] = request.form[key]
					pref_table.append(int(request.form[key]))
				except:
					slider_dict[key] = 1
					pref_table.append(1)
			
			prob_df = get_side_effect_probabilities(tuple(slider_names), indication, conn)
			prob_table = pd.pivot_table(prob_df, 'effect_proportion', rows='side_effect', cols='medicinalproduct')
			prob_table = prob_table.fillna(0)
			#return str(pref_table)
			dot_product = np.dot(pref_table, prob_table)
			medicinalproducts = list(prob_table.columns.values)
			score_df = pd.DataFrame(dot_product, index=medicinalproducts, columns=['score'])
			score_df=score_df.sort_index(by=['score'])
			recommendation = score_df.iloc[0].name
			
		return render_template('RxFx.html', 
			indication=indication, 
			slider_dict=slider_dict,
			recommendation=recommendation)

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
