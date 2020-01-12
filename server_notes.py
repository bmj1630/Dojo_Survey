from flask import Flask, render_template, request, redirect, session
from mysqlconnection import connectToMySQL
app = Flask(__name__)
#1. 3 tables, nina, location, language, loc & lang FK goes on ninja table
#2. populate the location and language table (using mySQL WB put loc and lang data in)
#3. set the id of those values as the value in your dropdowns

@app.route('/')
def dojo_form():
    """
    to show the dropdown of options and form
    use info from db and jinja to show the dropdown values, set lang/loc PK as values in drop down
    """
    query = "SELECT * FROM location"
    mysql = connectToMySQL("dojo_survey_validation")
    locations = mysql.query_db(query)
    query = "SELECT * FROM language"
    mysql = connectToMySQL("dojo_survey_validation")
    languages = mysql.query_db(query)
    return render_template('index.html', locations_for_templates = locations, languages_for_templates = languages)

@app.route('/users', methods=['POST'])
def dojo_survey():
    """
    when user submits form, they are passing as params (lang PK, loc PK, name, comment)
    using this information, creating a query associating a ninja with a lang, loc
    when query runs sucessfully, the PK of the ninja that was just inserted will be returned
    using that ninja PK, interpolate into a redirect url to show the ninja
    """
    form_name = request.form['name']
    location_choice = request.form['location'] # foreign key
    language_choice = request.form['language'] # foreign key
    comment_description = request.form['comment']
    mysql = connectToMySQL("dojo_survey_validation")
    query = "INSERT INTO ninja (name, location_id, language_id, created_at, updated_at) VALUES (%(fn)s, %(loc)s, %(lang)s, NOW(), NOW());"
    data = {
        "name": form_name,
        "loc": location_choice,
        "lang": language_choice,
    }
    ninja_id = mysql.query_db(query)
    return redirect("/results/{}".format(ninja_id))

@app.route("/results/<ninja_id>")
def show_results(ninja_id):
    """
    using ninja PK argument, <ninja_id>, select that ninja and using jinja2 template ninja result into html
    """
    query = "SELECT " # get the ninja based on ninja id
    data = {} # ninja id
    mysql = # connect to mysql 
    ninja = mysql.query_db(query, data)
    return render_template ('submitted_info.html', ninja = ninja) # [{ninja_data: "stuff"}]
if __name__ == "__main__":
    app.run(debug = True)