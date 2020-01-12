from flask import Flask, render_template, request, redirect, session, flash
import re
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key = "keep it secret"

@app.route('/')
def dojo_form():
    query = "SELECT * FROM location"
    mysql = connectToMySQL("dojo_survey_validation")
    locations = mysql.query_db(query)
    query = "SELECT * FROM language"
    mysql = connectToMySQL("dojo_survey_validation")
    languages = mysql.query_db(query)
    return render_template('index.html', locations_for_templates = locations, languages_for_templates = languages)

@app.route('/users', methods=['POST'])
def dojo_survey():
    is_valid = True
    if len(request.form['name']) < 1:
    	is_valid = False
    	flash("Enter a real name, idiot")
    if is_valid:
        form_name = request.form['name']
        location_choice = request.form['locations']
        language_choice = request.form['languages']
        comment_description = request.form['comment']
        mysql = connectToMySQL("dojo_survey_validation")
        query = "INSERT INTO ninja (name, location_id, language_id, created_at, updated_at) VALUES (%(name)s, %(loc)s, %(lang)s, NOW(), NOW());"
        data = {
            "name": form_name,
            "loc": location_choice,
            "lang": language_choice
        }
        ninja_id = mysql.query_db(query, data)
        flash("User entry successful!")
    return redirect("/results/{}".format(ninja_id))

@app.route("/results/<ninja_id>")
def results_page(ninja_id):
    query = "SELECT * FROM ninja JOIN location on location.id = ninja.location_id JOIN language on language.id = ninja.language_id WHERE ninja.id = %(nj)s;"
    data = {
        "nj": ninja_id
    }
    mysql = connectToMySQL("dojo_survey_validation")
    ninja = mysql.query_db(query, data)
    return render_template("submitted_info.html", ninja = ninja[0])

if __name__ == "__main__":
    app.run(debug = True)