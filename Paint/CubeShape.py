from LineShape import LineForm
from RectangleShape import RectangleForm

class CubeForm(LineForm, RectangleForm):
    def __init__(self, x1, y1, x2, y2, outline="black", fill="", dash=None):
        super().__init__(x1, y1, x2, y2, outline, fill, dash)
        self.outline = outline
        self.fill = ""
        self.dash = dash

    def draw(self, canvas, x1=None, y1=None, x2=None, y2=None):
        height = abs(self.y2 - self.y1)
        offset = height // 3
        backBottomLeft = (self.x1 + offset, self.y1 - offset)
        backBottomRight = (self.x2 + offset, self.y1 - offset)
        backTopLeft = (self.x1 + offset, self.y2 - offset)
        backTopRight = (self.x2 + offset, self.y2 - offset)
        RectangleForm.draw(self, canvas, self.x1, self.y1, self.x2, self.y2)
        RectangleForm.draw(self, canvas, backBottomLeft[0], backBottomLeft[1], backTopRight[0], backTopRight[1])
        LineForm.draw(self, canvas, self.x1, self.y1, backBottomLeft[0], backBottomLeft[1])
        LineForm.draw(self, canvas, self.x2, self.y1, backBottomRight[0], backBottomRight[1])
        LineForm.draw(self, canvas, self.x1, self.y2, backTopLeft[0], backTopLeft[1])
        LineForm.draw(self, canvas, self.x2, self.y2, backTopRight[0], backTopRight[1])