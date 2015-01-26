__author__ = 'simranjitsingh'

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash


app = Flask(__name__)
app.debug = True


@app.route('/')
def show_index():
    var = "from python script"
    return render_template('index2.html',var=var)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10080)
