class ArrowForm:
    def __init__(self, x1, y1, x2, y2, outline="black", fill="", dash=None):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.outline = outline
        self.fill = fill
        self.dash = dash

    def draw(self, canvas):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.outline, dash=self.dash, width=2)
        arrowL = 15
        arrowW = 5
        dx = self.x2 - self.x1
        dy = self.y2 - self.y1
        lineLength = (dx ** 2 + dy ** 2) ** 0.5
        if lineLength == 0:  # Avoid division by zero
            return
        # Normalize the line vector
        ux = dx / lineLength
        uy = dy / lineLength
        # Calculate the triangle vertices
        point1 = (self.x2, self.y2)
        point2 = (self.x2 - arrowL * ux + arrowW * uy, self.y2 - arrowL * uy - arrowW * ux)
        point3 = (self.x2 - arrowL * ux - arrowW * uy, self.y2 - arrowL * uy + arrowW * ux)

        canvas.create_polygon([point1, point2, point3], outline=self.outline, fill=self.fill)