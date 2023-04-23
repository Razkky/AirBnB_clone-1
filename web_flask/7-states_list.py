#!/usr/bin/python3
import sys
sys.path.append("..")
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)

@app.route("/states_list")
def state():
    all_states = storage.all(State)
    all_states = list(all_states.values())
    print(all_states)
    all_states.sort(key=lambda state: state.name)
    print(all_states)
    return render_template("7-states_list.html", all_states=all_states)


@app.teardown_appcontext
def tear_down(context):
    storage.close()


if __name__ == "__main__":
    app.run(debug=True)


