#!/usr/bin/python3
"""This script creates a Flask web application listening on 0.0.0.0"""
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    """Display Hello HBNB"""
    return "Hello HBNB!"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
