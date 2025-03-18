import tkinter as tk
from tkinter import colorchooser, IntVar
from Tooltip import Tooltip

class Toolbar(tk.Frame):
    def __init__(self, parent, setShapeCallback, buttonData, setColorCallback, setFillColorCallback, setLineStyleCallback):
        super().__init__(parent, bg="#f0f0f0", relief=tk.RAISED)
        self.parent = parent
        self.setShapeCallback = setShapeCallback
        self.setColorCallback = setColorCallback
        self.setFillColorCallback = setFillColorCallback
        self.setLineStyleCallback = setLineStyleCallback
        self.activeButton = None
        self.activeLineStyle = "solid"
        self.buttons = {}
        self.lineStyleButtons = {}
        self.buttonData = buttonData
        self.currentColor = "black"
        self.currentFillColor = "white"
        self.fillEnabled = IntVar(value=0)
        self.initializeButtons()

    def initializeButtons(self):
        # Create a container to center the buttons
        centerFrame = tk.Frame(self, bg="#f0f0f0")
        centerFrame.pack(side=tk.TOP, expand=True)
        # Add Undo button, line style buttons, and shape selection buttons to the center
        leftSpacer = tk.Frame(centerFrame, width=50, bg="#f0f0f0")
        leftSpacer.pack(side=tk.LEFT, expand=True)
        # Undo button
        self.addUndoButton()
        # Add line style buttons
        self.addLineStyleButtons(centerFrame)
        # Shape selection buttons
        for shapeType, data in self.buttonData.items():
            button = self.createButton(shapeType, data['image'])
            button.pack(side=tk.LEFT, padx=2, pady=2, in_=centerFrame)
            self.buttons[shapeType] = button
            Tooltip(button, f"Shape: {shapeType}")  # Add tooltip
        rightSpacer = tk.Frame(centerFrame, width=50, bg="#f0f0f0")
        rightSpacer.pack(side=tk.RIGHT, expand=True)
        # Add color and fill selection buttons to the right
        self.addColorElements()

    def createButton(self, shapeType, image):
        button = tk.Button(self, image=image, width=50, height=30, borderwidth=2)
        button.config(command=lambda: self.onButtonClick(shapeType, button))
        return button

    def addColorElements(self):
        colorFrame = tk.Frame(self)
        colorFrame.pack(side=tk.RIGHT, padx=5, pady=2)
        self.colorButton = tk.Button(colorFrame, text="", bg=self.currentColor, width=2, height=1, command=self.chooseLineColor)
        self.colorButton.grid(row=0, column=0, padx=2)
        Tooltip(self.colorButton, "Select outline color")
        colorLabel = tk.Label(colorFrame, text="Color", bg="#f0f0f0")
        colorLabel.grid(row=1, column=0)
        self.fillColorButton = tk.Button(colorFrame, text="", bg=self.currentFillColor, width=2, height=1, command=self.chooseFillColor)
        self.fillColorButton.grid(row=0, column=1, padx=2)
        Tooltip(self.fillColorButton, "Select fill color")
        fillLabel = tk.Label(colorFrame, text="Fill", bg="#f0f0f0")
        fillLabel.grid(row=1, column=1)
        # Checkbox to enable/disable fill
        fillCheckbox = tk.Checkbutton(colorFrame, text="No Fill", variable=self.fillEnabled, onvalue=0, offvalue=1,command=self.toggleFillColor, bg="#f0f0f0")
        fillCheckbox.grid(row=2, column=0, columnspan=2)
        Tooltip(fillCheckbox, "Enable/disable fill")

    def addLineStyleButtons(self, parentFrame):
        solidLineButton = tk.Button(parentFrame, text="─", width=4, height=2, relief=tk.SUNKEN, command=lambda: self.setLineStyle("solid"))
        solidLineButton.pack(side=tk.LEFT, padx=2, pady=2)
        self.lineStyleButtons["solid"] = solidLineButton
        Tooltip(solidLineButton, "Solid line")
        dashedLineButton = tk.Button(parentFrame, text="--", width=4, height=2, command=lambda: self.setLineStyle("dashed"))
        dashedLineButton.pack(side=tk.LEFT, padx=2, pady=2)
        self.lineStyleButtons["dashed"] = dashedLineButton
        Tooltip(dashedLineButton, "Dashed line")

    def addUndoButton(self):
        undoIcon = tk.PhotoImage(file="images/undo.png").subsample(12, 12)  # Add PNG icon
        undoButton = tk.Button(self, image=undoIcon, command=self.undo)
        undoButton.image = undoIcon  # Keep a reference to the image
        undoButton.pack(side=tk.LEFT, padx=2, pady=2)
        Tooltip(undoButton, "Undo action (Ctrl + Z)")  # Tooltip for dashed line

    def setLineStyle(self, style):
        self.activeLineStyle = style
        self.setLineStyleCallback(style)
        # Update button appearance
        for lineStyle, button in self.lineStyleButtons.items():
            if lineStyle == style:
                button.config(relief=tk.SUNKEN)
            else:
                button.config(relief=tk.RAISED)

    def chooseLineColor(self):
        colorCode = colorchooser.askcolor(title="Choose line color")[1]
        if colorCode:
            self.setColorCallback(colorCode)  # Set line color in the editor
            self.colorButton.config(bg=colorCode)  # Update button color

    def chooseFillColor(self):
        if self.fillEnabled.get() == 1:  # Fill is enabled
            colorCode = colorchooser.askcolor(title="Choose fill color")[1]
            if colorCode:
                self.setFillColorCallback(colorCode)  # Set fill color in the editor
                self.fillColorButton.config(bg=colorCode)  # Update button color

    def toggleFillColor(self):
        if self.fillEnabled.get() == 0:  # Fill is disabled
            self.setFillColorCallback("")  # Set empty string for fill
            self.fillColorButton.config(bg="white", state=tk.DISABLED)  # Disable fill color button
        else:
            self.setFillColorCallback(self.currentFillColor)  # Restore current fill color
            self.fillColorButton.config(state=tk.NORMAL)  # Enable fill color button

    def undo(self):
        """Calls the method to remove the last shape from the editor."""
        self.parent.shapeEditor.undo()

    def onButtonClick(self, shapeType, button):
        if self.activeButton != button:
            self.setShapeCallback(shapeType)
            self.updateActiveButton(button)

    def updateActiveButton(self, button):
        if self.activeButton:
            self.activeButton.config(relief=tk.RAISED)
        button.config(relief=tk.SUNKEN)
        self.activeButton = button