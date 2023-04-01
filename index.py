from flask import Flask, render_template, request, jsonify
from flask import flash, redirect, url_for
from config import Config
from forms import LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from AOGCpy3 import TextChecker
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
import models, routes

@app.route('/',methods=['GET', 'POST'])
@app.route('/index', methods=['GET','POST'])
def index():
	return render_template('index.html')

@app.route('/about', methods=['GET', 'POST'])
def about():
	return render_template('about.html')

@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
	return render_template('contact_us.html')


# @app.route('/process', methods=['POST'])
# def process():

# 	name = request.form['name']

# 	if name:
# 		#result = initial(name)
# 		spellError = spell_error(name)
# 		#print("Total", spellError)
# 		return jsonify({'errorWord' : spellError})

# 	return jsonify({'error' : 'Missing data!'})


@app.route('/process', methods=['GET', 'POST'])
def process():

	text = request.form['userText']
	print("Text: " + text)

	if text:
		textcheckerobj = TextChecker.TextChecker()
		result = textcheckerobj.check(text)
		
		errorSpellList = []
		errorGrammarList = []

		#print(result)
		# result = {'spell':{'akm':['akkam', 'akkamitti'], 'man':['mana', 'manaa'], 'esa':['eessa','eessaa']}, 'grammar': {'dhufte': ['Use another verb']}}
		# result = {'spell':{'akm':['akkam', 'akkamitti'], 'man':['mana', 'manaa'], 'esa':['eessa','eessaa']}, 'grammar': [['dhufte','Use another verb',"Example"],['dhufte','Use another verb',"Example"]]}
		print(result)
		spell = result["spell"]
		print(spell)
		grammar = result["grammar"]
		print(grammar)

		for s in spell.keys():
			errorSpellList.append(s)
		
		for g in grammar.keys():
			errorGrammarList.append(g)

		# print(errorSpellList)
		# print(errorGrammarList)
		# print(spell)

		return jsonify({'errorSpellList' : errorSpellList,'errorAndSuggestionSpellList' : spell,
		 'grammar' : grammar, 'errorGrammarList' : errorGrammarList, 'errorAndSuggestionGrammarList' : grammar})

	return jsonify({'error' : 'Missing data!'})



@app.route('/_spell_suggest/', methods=['POST'])
def _spell_suggest():
	
	error_word = request.form['error_word']
	suggest = request.form["suggestion"]
	

	if error_word:

		suggestList = []

		suggestList = suggest.split(',')

		return jsonify({'suggestion' : render_template('word_suggestion.html', word_candidates=suggestList,error_word = error_word)})

	return jsonify({'error' : 'No Suggestion!'})



@app.route('/_grammar_suggest/', methods=['GET', 'POST'])
def _grammar_suggest():
	
	error_word = request.form['error_word_Grammar']
	suggest = request.form["grammarSuggestion"]
	

	if error_word:
		suggestList = []

		suggestList = suggest.split(',')

		return jsonify({'suggestion' : render_template('grammar_suggestion.html', grammar_candidates=suggestList,error_word = error_word)})

	return jsonify({'error' : 'No Suggestion!'})

if __name__ == '__main__':
	app.run(debug=True)

# # @app.route('/admin', methods=['GET', 'POST'])
# @app.route('/login', methods=['GET', 'POST'])
# def login():
# 	form = LoginForm()
# 	if form.validate_on_submit():
# 		flash('Login requested for user {}, remember_me={}'.format(
# 			form.username.data, form.remember_me.data))
# 		return redirect(url_for('index'))
# 	return render_template('index.html', title='Sign In', form=form)