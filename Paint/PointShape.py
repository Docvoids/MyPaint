from Shape import Shape

class PointForm(Shape):
    def __init__(self, x, y, x2=None, y2=None, outline="black", fill="black", dash=None):
        super().__init__(outline, fill)
        self.x = x
        self.y = y
        self.size = 2
        self.dash = None

    def draw(self, canvas):
        canvas.create_oval(
            self.x - self.size, self.y - self.size,
            self.x + self.size, self.y + self.size,
            fill=self.outline, outline=self.outline
        )