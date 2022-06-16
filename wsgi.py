from flask import Flask, send_file, request
from experiments.run_experiments import start_experiments
import shutil
import os
import json

application = Flask(__name__,  static_url_path='')

os.chdir("./src")


@application.route("/", methods=['GET', 'POST', 'DELETE', 'PATCH'])
def hello():
    if request.method == 'POST':
        start_experiments(request.json)
        shutil.make_archive('../experiments', 'zip', '../output')
        return send_file('experiments.zip')
    elif request.method == 'PATCH':
        start_experiments()
        shutil.make_archive('../experiments', 'zip', '../output')
        return send_file('experiments.zip')
    elif request.method == "DELETE":
        shutil.rmtree('../output')
        return "deleted"
    else:
        return "hi"


@application.route("/newexp", methods=['PUT'])
def change():
    with open(f'../experiments/experiments.json', 'w') as fp:
        json.dump(request.json, fp)
    return "Changed"


@application.route("/getfiles", methods=['GET'])
def getfiles():
    shutil.make_archive('../experiments', 'zip', '../output')
    return send_file('experiments.zip')


if __name__ == "__main__":
    os.environ['FLASK_ENV'] = 'development'
    application.run(debug=True)
