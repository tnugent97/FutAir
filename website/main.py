from web import create_app
from flask import Flask
from flask import Markup
from flask import Flask
from flask import render_template

app = create_app('dev')

if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0",port=8081, threaded=True)