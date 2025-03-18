class Shape:
    def __init__(self, outline="black", fill="", dash=None):
        self.outline = outline
        self.fill = fill
        self.dash = dash

    def draw(self, canvas):
        return