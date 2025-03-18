import tkinter as tk

class MyEditor(tk.Canvas):
    _instance = None  # Static variable for Singleton instance

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, parent, app, bg="white"):
        if not hasattr(self, "initialized"):
            super().__init__(parent, bg=bg, scrollregion=(0, 0, 2000, 2000))
            self.parent = parent
            self.app = app
            self.shapes = []
            self.currentShape = None
            self.shapeClass = None
            self.startCoords = (None, None)
            self.currentColor = "black"
            self.currentFillColor = ""
            self.lineStyle = "solid"
            # Scrollbar bindings
            self.hScrollbar = tk.Scrollbar(parent, orient=tk.HORIZONTAL, command=self.xview)
            self.hScrollbar.pack(side=tk.BOTTOM, fill=tk.X)
            self.vScrollbar = tk.Scrollbar(parent, orient=tk.VERTICAL, command=self.yview)
            self.vScrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            self.config(xscrollcommand=self.hScrollbar.set, yscrollcommand=self.vScrollbar.set)
            self.setupBindings()

    def finalizeCurrentShape(self, x, y):
        if not self.shapeClass:
            return
        if self.shapeClass.__name__ == "CurveForm":
            self.shapes.append(self.currentShape)
            self.app.addShapeToTable((
                "Curve",
                "-", "-", "-", "-",
                self.currentColor,
                self.currentFillColor,
                "solid" if self.lineStyle == "solid" else "dash",
                self.currentShape.points
            ))
            self.currentShape = None
        else:
            dash = None if self.lineStyle == "solid" else (3, 3)
            finalizedShape = self.shapeClass(
                self.startCoords[0], self.startCoords[1], x, y,
                outline=self.currentColor, fill=self.currentFillColor, dash=dash
            )
            self.shapes.append(finalizedShape)
            shapeName = self.shapeClass.__name__.replace("Form", "")
            x1, y1 = self.startCoords
            x2 = "-" if shapeName == "Point" else x
            y2 = "-" if shapeName == "Point" else y
            self.app.addShapeToTable(( shapeName, x1, y1, x2, y2, self.currentColor, self.currentFillColor, "solid" if self.lineStyle == "solid" else "dash"))
        print(self.app.shapeData)
        self.currentShape = None
        self.startCoords = (None, None)

    def setupBindings(self):
        self.bind("<Button-1>", self.onMouseDown)
        self.bind("<B1-Motion>", self.onMouseMove)
        self.bind("<ButtonRelease-1>", self.onMouseUp)

    def setShapeType(self, shapeClass):
        self.shapeClass = shapeClass

    def setCurrentColor(self, color):
        self.currentColor = color

    def setCurrentFillColor(self, color):
        self.currentFillColor = color

    def setLineStyle(self, style):
        self.lineStyle = style

    def onMouseDown(self, event):
        if not self.shapeClass:
            return
        x, y = self.canvasx(event.x), self.canvasy(event.y)  # Account for scrolling
        if self.shapeClass.__name__ == "CurveForm":
            if not self.currentShape:
                self.currentShape = self.shapeClass(outline=self.currentColor,dash=(5, 5) if self.lineStyle == "dashed" else None)
            self.currentShape.addPoint(x, y)
        else:
            # For other shapes
            self.startCoords = (x, y)
            self.currentShape = self.shapeClass(x, y, x, y, outline=self.currentColor, fill=self.currentFillColor)

    def onMouseMove(self, event):
        if self.currentShape and self.shapeClass.__name__ == "CurveForm":
            x, y = self.canvasx(event.x), self.canvasy(event.y)
            self.currentShape.addPoint(x, y)
            self.redraw()
        elif self.currentShape:
            dash = None if self.lineStyle == "solid" else (3, 3)
            self.updateCurrentShape(self.canvasx(event.x), self.canvasy(event.y))
            self.currentShape.dash = dash
            self.redraw()

    def onMouseUp(self, event):
        self.finalizeCurrentShape(self.canvasx(event.x), self.canvasy(event.y))
        self.redraw()

    def updateCurrentShape(self, x, y):
        self.currentShape.x2, self.currentShape.y2 = x, y

    def undo(self):
        if not self.app.undoStack:
            # If the stack is empty, just remove the last shape
            if self.shapes:
                self.shapes.pop()
                if self.app.shapeData:
                    self.app.shapeData.pop()
                self.redraw()
            return
        lastState = self.app.undoStack.pop()
        self.shapes = lastState["shapes"]
        self.app.shapeData = lastState["shapeData"]
        self.redraw()

    def saveState(self):
        state = {
            "shapes": list(self.shapes),  # Copy the list of shapes
            "shapeData": list(self.app.shapeData)  # Copy shapeData
        }
        self.app.undoStack.append(state)

    def redraw(self):
        self.delete("all")
        for shape in self.shapes:
            shape.draw(self)
        if self.currentShape:
            self.currentShape.draw(self)
