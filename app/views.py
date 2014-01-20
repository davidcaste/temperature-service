from flask import redirect, render_template, url_for
from app import app
from models import read_logs

import datetime


@app.route('/')
@app.route('/index')
def index():
    now = datetime.datetime.now()
    return redirect('%s/%s/%s' % (now.year, now.month, now.day))


@app.route('/<int:year>/<int:month>/<int:day>')
def daily_temperature(year, month, day):
    indoor, outdoor = read_logs(year, month, day)
    return render_template('temperature.html',
                           title='Daily',
                           period='day',
                           indoor=indoor,
                           outdoor=outdoor)


@app.route('/<int:year>/<int:month>')
def monthly_temperature(year, month):
    indoor, outdoor = read_logs(year, month)
    return render_template('temperature.html',
                           title='Monthly',
                           period='month',
                           indoor=indoor,
                           outdoor=outdoor)


@app.route('/<int:year>')
def anual_temperature(year):
    indoor, outdoor = read_logs(year)
    return render_template('temperature.html',
                           title='Annual',
                           period='year',
                           indoor=indoor,
                           outdoor=outdoor)