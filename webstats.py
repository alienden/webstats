from flask import Flask
from flask import render_template
from flask import jsonify
from influxdb import InfluxDBClient

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('settings.cfg', silent=True)

@app.route("/")
def graph():
    client = InfluxDBClient(host=app.config['INFLUX_HOST'], port=app.config['INFLUX_PORT'], database=app.config['INFLUX_DATABASE'])
    query = client.query('select time, power_consumption from W where time > now() - 24h')
    return render_template('index.html',
                           results=query.get_points())

if __name__ == "__main__":
    app.run(host='0.0.0.0')
