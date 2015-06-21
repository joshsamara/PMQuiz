#!/usr/bin/env python
# encoding: utf-8
from flask import Flask, render_template, request
from logic import choose_tools, ALL_TOOLS
app = Flask(__name__)


# Home Page
@app.route("/")
def home():
    return render_template('home.html')


# Quiz Page
@app.route("/quiz", methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        form_data = {k: v[0] for k, v in dict(request.form).iteritems()}
        tool_data, notes = choose_tools(form_data)
        return results(True, tool_data, notes)
    else:
        return render_template('quiz.html')


# Results Page
@app.route("/results")
def results(recommend=False, tool_data=None, notes=None):
    if tool_data is None:
        tool_data = ALL_TOOLS
    if notes is None:
        notes = []
    return render_template('results.html',
                           recommend=recommend,
                           tool_data=tool_data,
                           notes=notes)


if __name__ == "__main__":
    app.run(debug=True)
