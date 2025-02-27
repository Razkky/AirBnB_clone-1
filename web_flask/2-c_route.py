#!/usr/bin/python3
"""This script creates a Flask web application listening on 0.0.0.0"""
from flask import Flask
app = Flask(__name__)
"""Instance of the application"""
app.url_map.strict_slashes = False


@app.route("/")
def index():
    """Display home page"""
    return "Hello HBNB!"


@app.route("/hbnb")
def hbnb():
    """Display hbnb page"""
    return "HBNB"


@app.route("/c/<text>")
def c(text):
    """Display C followed by value of text"""
    return "C {}".format(text.replace("_", " "))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
