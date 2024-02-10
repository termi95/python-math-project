import base64
import io
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from model.model import Line, Point
import json


def orientation(p: Point, q: Point, r: Point):
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    if val == 0:
        return 0
    return 1 if val > 0 else 2


def on_segment(p: Point, q: Point, r: Point):
    return (
        q.x <= max(p.x, r.x)
        and q.x >= min(p.x, r.x)
        and q.y <= max(p.y, r.y)
        and q.y >= min(p.y, r.y)
    )


def do_intersect(line1: Line, line2: Line):
    o1 = orientation(line1.start, line1.end, line2.start)
    o2 = orientation(line1.start, line1.end, line2.end)
    o3 = orientation(line2.start, line2.end, line1.start)
    o4 = orientation(line2.start, line2.end, line1.end)

    if o1 != o2 and o3 != o4:
        return True

    if o1 == 0 and on_segment(line1.start, line2.start, line1.end):
        return True

    if o2 == 0 and on_segment(line1.start, line2.end, line1.end):
        return True

    if o3 == 0 and on_segment(line2.start, line1.start, line2.end):
        return True

    if o4 == 0 and on_segment(line2.start, line1.end, line2.end):
        return True

    return False

def get_intersection_point(line1: Line, line2: Line):
    p1, q1 = line1.start, line1.end
    p2, q2 = line2.start, line2.end

    # Sprawdzenie, czy odcinki mają wspólny koniec
    if p1.x == p2.x and p1.y == p2.y:
        return p1
    elif p1.x == q2.x and p1.y == q2.y:
        return p1
    elif q1.x == p2.x and q1.y == p2.y:
        return q1
    elif q1.x == q2.x and q1.y == q2.y:
        return q1

    a1 = q1.y - p1.y
    b1 = p1.x - q1.x
    c1 = a1 * p1.x + b1 * p1.y

    a2 = q2.y - p2.y
    b2 = p2.x - q2.x
    c2 = a2 * p2.x + b2 * p2.y

    determinant = a1 * b2 - a2 * b1

    if determinant == 0:
        return None

    x = (b2 * c1 - b1 * c2) / determinant
    y = (a1 * c2 - a2 * c1) / determinant

    return Point(x, y)


def plot_line(line: Line, label: str, isIntersect: bool):
    plt.plot(
        [line.start.x, line.end.x],
        [line.start.y, line.end.y],
        marker="o",
        label=label,
        linewidth=1.5 if isIntersect else 1,
    )


def plot_intersection_dot(intersection_point: Point):
    print(type(intersection_point))
    plt.plot(
        intersection_point.x,
        intersection_point.y,
        marker="o",
        color="red",
        label="Przecięcie",
        zorder=4,
    )

def plot_intersection_line(intersection_line: Line):
    plt.plot(
        [intersection_line.start.x, intersection_line.end.x],
        [intersection_line.start.y, intersection_line.end.y],
        marker="o",
        color="red",
        label="wpólny odcinek",
        zorder=4,
    )
    
def get_intersection_line(line1:Line, line2:Line):
    start_x = max(line1.start.x, line2.start.x)
    end_x = min(line1.end.x, line2.end.x)
    
    start_y = max(line1.start.y, line2.start.y)
    end_y = min(line1.end.y, line2.end.y)
    if start_x >= end_x or start_y >= end_y:
        return None
    else:
        return Line(Point(start_x,start_y),Point(end_x,end_y))
        

# Generuje wykres
def get_chart_with_info(line1: Line, line2: Line):
    data = {}
    isIntersect = False
    intersection_point = None
    intersection_line = None
    plt.figure()
    if do_intersect(line1, line2):
        isIntersect = True
        intersection_point = get_intersection_point(line1, line2)
        intersection_line = get_intersection_line(line1, line2)
        print(intersection_point)
        print(intersection_line)
        if intersection_point != None and intersection_line == None:
            plot_intersection_dot(intersection_point)
        
        if intersection_line != None:
            plot_intersection_line(intersection_line)
    plot_line(line1, "Odcinek 1", isIntersect)
    plot_line(line2, "Odcinek 2", isIntersect)

    plt.xlabel("Oś X")
    plt.ylabel("Oś Y")
    plt.title("Przecięcie odcinków")
    plt.legend()
    plt.grid(True)
    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format="jpg")
    my_stringIObytes.seek(0)
    chart = base64.b64encode(my_stringIObytes.read()).decode()
    data["line1"] = line1.get_line_as_json()
    data["line2"] = line2.get_line_as_json()
    data["isIntersect"] = isIntersect
    if intersection_point != None and intersection_line == None:       
        data["intersection_point"] =  intersection_point.get_point_as_json()
    if intersection_line != None:
         data["intersection_line"] = intersection_line.get_line_as_json()
    data["chart"] = chart
    return json.dumps(data)
