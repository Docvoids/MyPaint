from Shape import Shape

class DiamondForm(Shape):
    def __init__(self, x1, y1, x2, y2, outline="black", fill="", dash=None):
        super().__init__(outline, fill, dash)
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        self.dash = dash

    def draw(self, canvas):
        xCenter = (self.x1 + self.x2) / 2
        yCenter = (self.y1 + self.y2) / 2
        points = [
            (xCenter, self.y1),  # Top corner
            (self.x2, yCenter),  # Right corner
            (xCenter, self.y2),  # Bottom corner
            (self.x1, yCenter)   # Left corner
        ]
        canvas.create_polygon(
            points,
            outline=self.outline,
            fill=self.fill,
            dash=self.dash,
            smooth=False
        )