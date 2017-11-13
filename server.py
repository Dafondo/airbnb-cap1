from flask import Flask, request, render_template, g, jsonify
import sqlite3

app = Flask(__name__)

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

@app.route('/calc', methods=['GET', 'POST'])
def calc():
    if request.method == 'POST':
        lat = float(request.form['lat'])
        lon = float(request.form['lon'])
        r = 0.001
        
        results = query_db('SELECT id, price, weekly_price, monthly_price FROM listings WHERE abs(latitude - %f) < %f and abs(longitude - %f) < %f' % (lat, r, lon, r))
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

        results = query_db('SELECT AVG(CAST(SUBSTR(price, 2) as FLOAT)) FROM listings WHERE reviews_per_month > 1 and abs(latitude - %f) < %f and abs(longitude - %f) < %f' % (lat, r, lon, r))
        optimalPrice = '%.2f' % results[0][0]

        return render_template('calculator.html', lat=lat, lon=lon, weeklyEst = weeklyEst, optimalPrice = optimalPrice)
    else:
        return render_template('calculator.html')

@app.route('/stats', methods=['GET'])
def stats():
    if request.method == 'GET':
        results = []
        for i in xrange(0, 3):
            results.append([])
        g1 = query_db('SELECT AVG(availability_30), AVG(review_scores_rating) FROM listings GROUP BY availability_30 ORDER BY availability_30 ASC')
        g2 = query_db('SELECT DISTINCT neighborhood_cleansed, AVG(CAST(SUBSTR(price, 2) as FLOAT)) FROM listings GROUP BY neighborhood_cleansed ORDER BY neighborhood_cleansed ASC')
        g3 = query_db('SELECT DISTINCT host_response_time, AVG(review_scores_communication) FROM listings GROUP BY host_response_time ORDER BY host_response_time ASC')
        for item in g1:
            if item[0] != 0:
                results[0].append([item[0], round(item[1],2)])
        for item in g2:
            results[1].append([item[0], round(float(item[1]),2)])
        for item in g3:
            if item[0] != '':
                results[2].append([item[0], round(item[1],2)])

        return jsonify(results)
        

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 80, debug = True)