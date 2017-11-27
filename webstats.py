from flask import Flask
from flask import render_template
from flask import jsonify
from influxdb import InfluxDBClient
import json
import plotly

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('settings.cfg', silent=True)

@app.route("/")
def graph():
    timestamps = []
    powervalues = []

    client = InfluxDBClient(host=app.config['INFLUX_HOST'], port=app.config['INFLUX_PORT'], database=app.config['INFLUX_DATABASE'])
    #get all the power measurments from InfluxDB for the last 24hr
    result = client.query("select time, power_consumption from W where time > now() - 24h tz('America/New_York')")

    datapoints = list(result.get_points())
    header_list = list(datapoints[0].keys())

    #get list of values for x,y axis
    for point in datapoints:
        timestamps.append(point['time'])
        powervalues.append(point['power_consumption'])

    #setup graph
    graphs = [
        dict(
            data=[
                dict(
                    x=timestamps,
                    y=powervalues,
                    type='scatter',
                    name='spline',
                ),
            ],
            layout=dict(
                title='Power Consumption from the PC outlet'
            )
        )
    ]

    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)


    return render_template('index.html',
                           graphJSON=graphJSON)

if __name__ == "__main__":
    app.run(host='0.0.0.0')