class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        
    def get_point_as_json(self):
        return {'x':self.x,'y':self.y}


class Line:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end
        
    def get_line_as_json(self):
        return {'start': self.start.get_point_as_json(), 'end': self.end.get_point_as_json()}