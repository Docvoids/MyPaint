import tkinter as tk
from tkinter import Menu
from MyEditor import MyEditor
from Toolbar import Toolbar
from Files import Files
from PointShape import PointForm
from LineShape import LineForm
from RectangleShape import RectangleForm
from EllipseShape import EllipseForm
from DumbbellShape import DumbbellForm
from CubeShape import CubeForm
from DiamondShape import DiamondForm
from CurveShape import CurveForm
from ArrowShape import ArrowForm

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RGR")
        self.geometry("1000x700")
        self.shapeClasses = self.initializeShapeClasses()
        self.shapeData = []
        self.undoStack = []
        self.toolbar = Toolbar(self, self.setShape, self.shapeClasses, self.setColor, self.setFillColor, self.setLineStyle)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        self.editorFrame = tk.Frame(self)  # Frame for the editor
        self.editorFrame.pack(fill=tk.BOTH, expand=True)
        self.shapeEditor = self.createEditor()
        self.files = Files(self, self.shapeEditor)
        self.createMenuBar()
        self.bindShortcuts()  # Bind shortcuts
        self.protocol("WM_DELETE_WINDOW", self.onClose)

    def initializeShapeClasses(self):
        return {
            "Curve": {"shape": CurveForm, "image": tk.PhotoImage(file="images/pencil.png").subsample(17, 17)},
            "Point": {"shape": PointForm, "image": tk.PhotoImage(file="images/point1.png").subsample(20, 20)},
            "Line": {"shape": LineForm, "image": tk.PhotoImage(file="images/line1.png").subsample(60, 60)},
            "Rectangle": {"shape": RectangleForm, "image": tk.PhotoImage(file="images/rectangle1.png").subsample(8, 8)},
            "Ellipse": {"shape": EllipseForm, "image": tk.PhotoImage(file="images/ellipse1.png").subsample(10, 10)},
            "Diamond": {"shape": DiamondForm, "image": tk.PhotoImage(file="images/romb.png").subsample(6, 6)},
            "Dumbbell": {"shape": DumbbellForm, "image": tk.PhotoImage(file="images/dumbbell1.png").subsample(10, 10)},
            "Cube": {"shape": CubeForm, "image": tk.PhotoImage(file="images/cube1.png").subsample(20, 20)},
            "Arrow": {"shape": ArrowForm, "image": tk.PhotoImage(file="images/arrow.png").subsample(6, 6)},
        }

    def createEditor(self):
        editor = MyEditor(self.editorFrame, app=self)  # Pass MainApp as app
        editor.pack(fill=tk.BOTH, expand=True)
        return editor

    def addShapeToTable(self, shapeData):
        self.shapeData.append(shapeData)

    def setColor(self, color):
        self.shapeEditor.setCurrentColor(color)  # Set line color in the editor

    def setFillColor(self, color):
        self.shapeEditor.setCurrentFillColor(color)  # Set fill color in the editor

    def setLineStyle(self, style):
        self.shapeEditor.setLineStyle(style)

    def createMenuBar(self):
        menuBar = Menu(self)
        self.config(menu=menuBar)
        self.addFileMenu(menuBar)

    def addFileMenu(self, menuBar):
        fileMenu = Menu(menuBar, tearoff=0)
        fileMenu.add_command(label="Save File",command=self.files.saveToCurrentFile)  # Save to current file
        fileMenu.add_command(label="Save File As",command=self.files.saveTableToFile)  # Save with new path selection
        fileMenu.add_command(label="Save PNG", command=self.files.saveSceneToPng)
        fileMenu.add_command(label="Open File", command=self.files.loadTableFromFile)  # Load file
        fileMenu.add_command(label="Clear Scene", command=self.clearEditor)
        menuBar.add_cascade(label="File", menu=fileMenu)

    def setShape(self, shapeType):
        self.shapeEditor.shapeClass = self.shapeClasses[shapeType]['shape']

    def clearEditor(self):
        self.shapeEditor.saveState()
        self.shapeEditor.delete("all")  # Clear all shapes from the canvas
        self.shapeEditor.shapes = []  # Reset the shapes list
        self.shapeData = []

    def onClose(self):
        self.destroy()

    def bindShortcuts(self):
        self.bind("<Control-s>", lambda event: self.files.saveToCurrentFile())  # Ctrl + S
        self.bind("<Control-z>", lambda event: self.shapeEditor.undo())  # Ctrl + Z

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()