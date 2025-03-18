from LineShape import LineForm
from EllipseShape import EllipseForm

class DumbbellForm(LineForm, EllipseForm):
    def __init__(self, x1, y1, x2, y2, dash=None, outline="black", fill="black", radius=10):
        super().__init__(x1, y1, x2, y2, dash)
        self.fill = fill
        self.outline = outline
        self.radius = radius
        self.dash = dash

    def draw(self, canvas, x1=None, y1=None, x2=None, y2=None):
        LineForm.draw(self, canvas)

        EllipseForm.draw(self, canvas, self.x1 - self.radius, self.y1 - self.radius, self.x1 + self.radius, self.y1 + self.radius)
        EllipseForm.draw(self, canvas, self.x2 - self.radius, self.y2 - self.radius, self.x2 + self.radius, self.y2 + self.radius)