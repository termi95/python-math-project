from flask import Flask, render_template, request, flash, redirect, session, url_for

from model.model import Line, Point
from services.services import get_chart_with_info

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dupa", methods=["POST"])
def get_Chart():
    data = request.get_json()
   
    line1 = Line(Point(data['lines'][0]['start']['x'],data['lines'][0]['start']['y']),Point(data['lines'][0]['end']['x'],data['lines'][0]['end']['y']))
    line2 = Line(Point(data['lines'][1]['start']['x'],data['lines'][1]['start']['y']),Point(data['lines'][1]['end']['x'],data['lines'][1]['end']['y']))
   
    return  get_chart_with_info(line1, line2)


if __name__ == "__main__":
    base_url = "http://127.0.0.1:5000"
    app.run(debug=True)

