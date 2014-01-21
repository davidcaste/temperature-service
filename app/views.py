from flask import abort, redirect, render_template
from app import app
from models import DaySample, read_logs

import datetime


@app.route('/')
@app.route('/index')
def index():
    now = datetime.datetime.now()
    return redirect('%s/%s/%s' % (now.year, now.month, now.day))


@app.route('/<int:year>/<int:month>/<int:day>')
def daily_temperature(year, month, day):
    try:
        samples = DaySample(year, month, day)
    except:
        abort(404)

    return render_template('temperature.html',
                           samples=samples)


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


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500