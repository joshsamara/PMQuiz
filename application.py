#!/usr/bin/env python
# encoding: utf-8
from flask import Flask, render_template, request
from yaml import load
from logic import choose_tools
app = Flask(__name__)

# Load tools from yaml
with open("tools.yaml", 'r') as stream:
    tools = load(stream)
    stream.close()


# Home Page
@app.route("/")
def home():
    return render_template('home.html')


# Quiz Page
@app.route("/quiz", methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        tool_data, notes = choose_tools(request.form)
        return results(True, tool_data, notes)
    else:
        return render_template('quiz.html')


# Results Page
@app.route("/results")
def results(recommend=False, tool_data=None, notes=None):
    if tool_data is None:
        tool_data = tools
    if notes is None:
        notes = []
    return render_template('results.html',
                           recommend=recommend,
                           tool_data=tool_data,
                           notes=notes)


if __name__ == "__main__":
    app.run(debug=True)
