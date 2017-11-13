from flask import Flask, request, render_template, g
import sqlite3
from math import pi

app = Flask(__name__)

# from . import config
# from instance import config

DATABASE = 'db/airbnb.db'

R = 6371000
def toRadians(degrees):
    return degrees * pi / 180

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE, check_same_thread=False)

    db.row_factory = sqlite3.Row

    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def root():
    if request.method == "GET":
        return render_template('index.html')

@app.route('/charts')
def charts():
    if request.method == "GET":
        return render_template('charts.html')

@app.route('/tables')
def tables():
    if request.method == "GET":
        return render_template('tables.html')

@app.route('/test')
def test():
    conn = get_db().cursor()
    lat = 37.769310377340766
    lon = -122.43385634488999
    results = query_db('SELECT id FROM listings WHERE latitude <= %f and longitude <= %f' % (lat, lon))
    # results = conn.execute('SELECT id FROM listings WHERE latitude <= %f and longitude <= %f' % (lat, lon)).fetchone()[0]
    returnVal = ''
    for result in results:
        returnVal += str(result['id']) + '\n'
    return returnVal

@app.route('/calc', methods=['GET', 'POST'])
def calc():
    if request.method == 'POST':
        lat = float(request.form['lat'])
        lon = float(request.form['lon'])
        r = 0.001
        # results = query_db('''\
        # SELECT * FROM listings WHERE (6371 * 2 * 
        # ATAN2(SQRT(SIN((latitude - %f)*PI/180/2) * SIN((latitude - %f)*PI/180/2) + COS(latitude)
        #  * COS(%f) * SIN((longitude - %f)*PI/180/2) * SIN((longitude - %f)*PI/180/2)),
        # SQRT(1 - (SIN((latitude - %f)*PI/180/2) * SIN((latitude - %f)*PI/180/2) + COS(latitude)
        #  * COS(%f) * SIN((longitude - %f)*PI/180/2) * SIN((longitude - %f)*PI/180/2)))))
        #  < %f''' % (lat, lat, lat, lon, lon, lat, lat, lat, lon, lon, r))
        results = query_db('SELECT * FROM listings WHERE abs(latitude - %f) < %f and abs(longitude - %f) < %f' % (lat, r, lon, r))
        if len(results) < 1:
            return render_template('calculator.html', lat=lat, lon=lon)
        returnVal = ''
        weeklyEst = 0
        for result in results:
            if(result['weekly_price']):
                weeklyEst += float(result['weekly_price'][1:].replace(',',''))
            elif(result['monthly_price']):
                weeklyEst += float(result['monthly_price'][1:].replace(',',''))/4
            else:
                weeklyEst += float(result['price'][1:].replace(',',''))*7
            returnVal += str(result['id']) + '   \n'
        weeklyEst /= len(results)
        weeklyEst = '%.2f' % round(weeklyEst,2)
        return render_template('calculator.html', lat=lat, lon=lon, weeklyEst = weeklyEst)
    else:
        return render_template('calculator.html')

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 80, debug = True)