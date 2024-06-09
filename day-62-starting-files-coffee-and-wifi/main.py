from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import pandas as pd
# import csv

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired(),URL()])
    open = StringField('Open', validators=[DataRequired()])
    closing = StringField('Closing', validators=[DataRequired()])
    coffee = SelectField('Coffee Rating', validators=[DataRequired()], choices=['0','1','2','3','4','5'])
    wifi = SelectField('Wifi', validators=[DataRequired()], choices=['0','1','2','3','4','5'])
    power = SelectField('Power', validators=[DataRequired()], choices=['0','1','2','3','4','5'])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
# noinspection PyPackageRequirements
@app.route("/")
def index():
    df = pd.read_csv('cafe-data.csv')
    list_of_rows = list()
    for indx, row in df.iterrows():
        d = row.to_dict()
        list_of_rows.append(d)
    print(list_of_rows[0])
    return render_template("index.html")


@app.route('/add',methods=['GET','POST'] )
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        new_listing = {
            'Cafe Name': form.cafe.data,
            'Location': form.location.data,
            'Open': form.open.data,
            'Closing': form.closing.data,
            'Coffee': form.coffee.data,
            'Wifi': form.wifi.data,
            'Power': form.power.data
        }
        output=''
        for v in new_listing.values():
            output += f'{v},'
        output = output[:-1]
        output+='\n'
        with open('cafe-data.csv', 'a')as csv:
            csv.writelines(output)
            message = "Cafe Submitted Successfully"
        return render_template('add.html',form=form, msg=message)
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    df = pd.read_csv('cafe-data.csv')
    list_of_rows = list()
    for indx, row in df.iterrows():
        d = row.to_dict()
        list_of_rows.append(d)
    return render_template('cafes.html', cafes=list_of_rows)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
