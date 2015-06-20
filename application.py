#!/usr/bin/env python
# encoding: utf-8
from flask import Flask, render_template, request
app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/quiz", methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        print request.form
        return render_template('quiz.html')
    else:
        return render_template('quiz.html')

if __name__ == "__main__":
    app.run(debug=True)
