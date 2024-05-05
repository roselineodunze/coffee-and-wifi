from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
import csv
import pandas

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Location URL', validators=[DataRequired()])
    open_time = StringField('open time', validators=[DataRequired()])
    close_time = StringField('closing time', validators=[DataRequired()])
    coffee = SelectField('coffee rating', choices=[('✘', '✘'), ('☕️', '☕️'), ('☕️☕️', '☕️☕️'), ('☕️☕️☕️', '☕️☕️☕️'), ('☕️☕️☕️☕️', '☕️☕️☕️☕️'), ('️☕️☕️☕️☕️☕️', '☕️☕️☕️☕️☕️')], validators=[DataRequired()])
    wifi = SelectField('wifi rating', choices=[('✘', '✘'), ('💪', '💪'), ('💪💪', '💪💪'), ('💪💪💪', '💪💪💪'), ('💪💪💪💪', '💪💪💪💪'), ('💪💪💪💪💪', '💪💪💪💪💪')], validators=[DataRequired()])
    power = SelectField('power outlet rating', choices=[('✘', '✘'), ('🔌', '🔌'), ('🔌🔌', '🔌🔌'), ('🔌🔌🔌', '🔌🔌🔌'), ('🔌🔌🔌🔌', '🔌🔌🔌🔌'), ('🔌🔌🔌🔌🔌', '🔌🔌🔌🔌🔌')], validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/add', methods=['GET','POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        cafe = form.cafe.data
        location = form.location.data
        open_time = form.open_time.data
        close_time = form.close_time.data
        coffee = form.coffee.data
        wifi = form.wifi.data
        power = form.wifi.data
        row = f"\n{cafe},{location},{open_time},{close_time},{coffee},{wifi},{power}"
        with open("cafe-data.csv", mode='a', newline='') as file:
            file.write(row)
        return redirect(url_for('add_cafe'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        headers = next(csv_data)
        cafes_data = []
        for row in csv_data:
            cafe_data = {}
            for header, value in zip(headers, row):
                cafe_data[header] = value
            cafes_data.append(cafe_data)
    return render_template('cafes.html', cafes=cafes_data)


if __name__ == '__main__':
    app.run(debug=True)
