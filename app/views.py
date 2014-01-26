from flask import abort, redirect, render_template
from app import app
from models import DaySample, MonthSample, YearSample, NonExistantLogsError

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
    except NonExistantLogsError:
        abort(404)
    except:
        abort(500)

    return render_template('day.html',
                           samples=samples)


@app.route('/<int:year>/<int:month>')
def monthly_temperature(year, month):
    try:
        samples = MonthSample(year, month)
    except NonExistantLogsError:
        abort(404)
    except:
        abort(500)

    return render_template('month.html',
                           samples=samples)


@app.route('/<int:year>')
def anual_temperature(year):
    try:
        samples = YearSample(year)
    except NonExistantLogsError:
        abort(404)
    except:
        abort(500)

    return render_template('year.html',
                           samples=samples)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500