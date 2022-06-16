from flask import Flask
from experiments.run_experiments import start_experiments

application = Flask(__name__)


@application.route("/")
def hello():
    import os
    cwd = os.getcwd()
    print(cwd)
    start_experiments()
    return "Hello World!"


if __name__ == "__main__":
    application.run()
