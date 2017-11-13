from flask import Flask
from flask import render_template
from flask import jsonify
from influxdb import InfluxDBClient

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('settings.cfg', silent=True)

@app.route("/")
def graph():
    client = InfluxDBClient(host=app.config['INFLUX_HOST'], port=app.config['INFLUX_PORT'])
    dbs = client.get_list_database()
    return render_template('index.html',
                           results=dbs)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
