from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, SelectField
from wtforms.validators import DataRequired, URL
from wtforms.widgets.html5 import TimeInput
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired(message="Compulsory field")])
    location = StringField('Cafe location on Google Maps(URL)', validators=[DataRequired(message="Compulsory field"),
                                                                            URL(message="Enter a valid Google Maps URL")])
    open_time = StringField('Opening Time e.g. 9AM',
                            validators=[DataRequired(message="Compulsory field")])
    close_time = StringField('Closing Time e.g. 8:30PM',
                             validators=[DataRequired(message="Compulsory field")])
    coffee_rating = SelectField('Coffee Rating ☕️', choices=['☕️' * i if i != 0 else '✘' for i in range(0, 6)],
                                validators=[DataRequired(message="Compulsory field")])
    wifi_rating = SelectField('Wifi Strength Rating 💪', choices=['💪' * i if i != 0 else '✘' for i in range(0, 6)],
                              validators=[DataRequired(message="Compulsory field")])
    power_rating = SelectField('Power Socket Accessibility 🔌',
                               choices=['🔌' * i if i != 0 else '✘' for i in range(0, 6)],
                               validators=[DataRequired(message="Compulsory field")])
    submit = SubmitField('Submit', )


# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
# e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


@app.route('/add', methods=['POST', 'GET'])
def add_cafe():
    form = CafeForm()

    if form.validate_on_submit():  # and request.method == 'POST'
        print("True")
        # print(type(form.cafe.data))

        with open('cafe-data.csv', newline='', encoding='utf8', mode='a') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow([form.cafe.data,
                             form.location.data,
                             form.open_time.data,
                             form.close_time.data,
                             form.coffee_rating.data,
                             form.wifi_rating.data,
                             form.power_rating.data])

        return redirect('cafes')

    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()

    return render_template('add.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
