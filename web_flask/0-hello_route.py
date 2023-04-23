#!/usr/bin/python3
"""This script creates a Flask web application listening on 0.0.0.0"""
from flask import Flask
"""Instance of the application"""
app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route("/")
def hello():
    """Display Hello HBNB"""
    return "Hello HBNB!"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
