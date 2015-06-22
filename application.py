#!/usr/bin/env python
# encoding: utf-8
import os
from flask import Flask, render_template, request
from logic import choose_tools, ALL_TOOLS
app = Flask(__name__)


# Home Page
@app.route("/")
def home():
    """Serve the basic home page."""
    return render_template('home.html')


# Quiz Page
@app.route("/quiz", methods=['GET', 'POST'])
def quiz():
    """Serve and handle the quiz form."""
    if request.method == 'POST':
        # Cleanup our form data into something more manageable
        form_data = {k: v[0] for k, v in dict(request.form).iteritems()}
        tool_data, notes = choose_tools(form_data)
        return results(True, tool_data, notes)
    else:
        return render_template('quiz.html')


# Results Page
@app.route("/results")
def results(recommend=False, tool_data=ALL_TOOLS, notes=None):
    """Serve the page for either all or recommended tools."""
    if notes is None:
        notes = []
    return render_template('results.html',
                           recommend=recommend,
                           tool_data=tool_data,
                           notes=notes)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
