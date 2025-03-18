from Shape import Shape

class CurveForm(Shape):
    def __init__(self, outline="black", fill="", dash=None):
        super().__init__(outline, fill, dash)
        self.x1, self.y1 = 0, 0
        self.x2, self.y2 = 0, 0
        self.points = []  # List of points for the curve

    def addPoint(self, x, y):
        self.points.append((x, y))

    def draw(self, canvas):
        if len(self.points) > 1:
            canvas.create_line(
                self.points,
                fill=self.outline,
                dash=self.dash,
                smooth=True  # Makes the curve smooth
            )