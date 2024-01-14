from flask import Flask, make_response, render_template, request


from model.model import Line, Point
from services.services import get_chart_with_info

app = Flask(__name__)


def is_float(value):
    if value is None:
        return False
    try:
        float(value)
        return True
    except:
        return False


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get-chart", methods=["POST"])
def get_Chart():
    data = request.get_json()

    if "lines" not in data:
        return make_response({"message": "lines not find in request"}, 400)
    elif len(data["lines"]) != 2:
        return make_response({"message": "Payloud must contain 2 lines"}, 400)

    lines = data["lines"]
    parsed_lines = []

    for index in range(2):
        if "start" not in lines[index] or "end" not in lines[index]:
            return make_response(
                {"message": "Line not contain start or end point."}, 400
            )
        if (
            "x" not in lines[index]["start"]
            or "y" not in lines[index]["start"]
            or "x" not in lines[index]["end"]
            or "y" not in lines[index]["end"]
        ):
            return make_response({"message": "Point not contain x or y."}, 400)
        if (
            not is_float(lines[index]["start"]["x"])
            or not is_float(lines[index]["start"]["y"])
            or not is_float(lines[index]["end"]["x"])
            or not is_float(lines[index]["end"]["y"])
        ):
            return make_response({"message": "x or y is not a number."}, 400)
        parsed_lines.append(
            Line(
                Point(
                    float(lines[index]["start"]["x"]), float(lines[index]["start"]["y"])
                ),
                Point(float(lines[index]["end"]["x"]), float(lines[index]["end"]["y"])),
            )
        )

    return get_chart_with_info(parsed_lines[0], parsed_lines[1])


if __name__ == "__main__":
    base_url = "http://127.0.0.1:5000"
    app.run(debug=True)
