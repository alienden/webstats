from flask import Flask
from flask import jsonify
from influxdb import InfluxDBClient

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('settings.cfg', silent=True)

@app.route("/")
def hello():
    client = InfluxDBClient(host=app.config['INFLUX_HOST'], port=app.config['INFLUX_PORT'])
    #print app.config['INFLUX_SETTINGS[HOST]']
    dbs = client.get_list_database()
    return jsonify(dbs)
#    return "<h1 style='color:blue'>Hello There You!</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
