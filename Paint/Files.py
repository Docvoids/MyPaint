import tkinter as tk
from PIL import Image, ImageDraw
from tkinter import filedialog, messagebox


class Files:
    def __init__(self, app, editor):
        self.app = app  # Reference to the main MainApp class
        self.editor = editor
        self.currentFilePath = None  # Current file path

    def saveToCurrentFile(self):
        if not self.currentFilePath:
            self.saveTableToFile()  # Open dialog to select a new file
        else:
            self._saveFile(self.currentFilePath)  # Save to the current file

    def saveTableToFile(self):
        file = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save File As"
        )
        if file:
            self.currentFilePath = file  # Save the file path
            self._saveFile(file)
            self.app.title(file)  # Update the window title

    def _saveFile(self, filePath):
        try:
            with open(filePath, "w") as file:
                # File header
                file.write("Shape\tx1\ty1\tx2\ty2\toutline\tfill\tstyle\tpoints\n")
                for row in self.app.shapeData:
                    shapeName, x1, y1, x2, y2, outline, fill, style = row[:8]
                    outline = outline if outline else "-"
                    fill = fill if fill else "-"
                    style = style if style else "solid"
                    if shapeName == "Curve":
                        # Save curve points
                        points = row[8]
                        pointsStr = ";".join(f"{p[0]},{p[1]}" for p in points)
                    else:
                        pointsStr = "-"
                    # Write the data row
                    file.write(f"{shapeName}\t{x1}\t{y1}\t{x2}\t{y2}\t{outline}\t{fill}\t{style}\t{pointsStr}\n")
            messagebox.showinfo("Success", f"Scene successfully saved to {filePath}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")

    def loadTableFromFile(self):
        file = filedialog.askopenfile(
            mode="r",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Open File"
        )
        if file:
            try:
                self.app.clearEditor()
                self.app.undoStack = []
                self.currentFilePath = file.name
                self.app.title(file.name)  # Update the window title

                lines = file.readlines()
                header = lines[0].strip().split("\t")
                if header != ["Shape", "x1", "y1", "x2", "y2", "outline", "fill", "style", "points"]:
                    raise ValueError("Invalid file format.")

                for lineNumber, line in enumerate(lines[1:], start=2):  # Line numbers start from 2
                    columns = line.strip().split("\t")
                    if len(columns) != 9:  # Check the number of columns
                        messagebox.showwarning(
                            "Warning",
                            f"Line {lineNumber} has an invalid format and will be skipped."
                        )
                        continue
                    shapeName, x1, y1, x2, y2, outline, fill, style, pointsStr = columns
                    x1, y1 = float(x1) if x1 != "-" else None, float(y1) if y1 != "-" else None
                    x2, y2 = float(x2) if x2 != "-" else None, float(y2) if y2 != "-" else None
                    outline = outline if outline != "-" else ""
                    fill = fill if fill != "-" else ""
                    dash = None if style == "solid" else (5, 5)
                    if shapeName == "Curve":
                        # Parse the list of points
                        points = [
                            tuple(map(float, p.split(",")))
                            for p in pointsStr.split(";") if pointsStr != "-"
                        ]
                        shape = self.app.shapeClasses[shapeName]["shape"](outline=outline, dash=dash)
                        shape.points = points  # Set the points
                    else:
                        shapeClass = self.app.shapeClasses[shapeName]["shape"]
                        shape = shapeClass(x1, y1, x2, y2, outline=outline, fill=fill, dash=dash)
                    self.app.shapeEditor.shapes.append(shape)
                    # Add data to the table
                    self.app.shapeData.append(
                        (shapeName, x1, y1, x2 if x2 else "-", y2 if y2 else "-", outline, fill, style,
                         points if shapeName == "Curve" else "-")
                    )
                self.app.shapeEditor.redraw()
                file.close()
                tk.messagebox.showinfo("Success", "Scene successfully loaded")
            except Exception as e:
                tk.messagebox.showerror("Error", f"Failed to load file: {e}")

    def saveSceneToPng(self):
        filePath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            title="Save Scene as PNG"
        )
        if not filePath:
            return
        image = Image.new("RGB", (2000, 2000), "white")
        draw = ImageDraw.Draw(image)
        # Iterate through all shapes and draw them on the image
        for shape in self.editor.shapes:
            if hasattr(shape, "points"):  # Curve
                draw.line(shape.points, fill=shape.outline, width=2, joint="curve")
            elif hasattr(shape, "x1") and hasattr(shape, "x2"):  # Rectangles, lines, and arrows
                if isinstance(shape, self.app.ArrowForm):
                    draw.line([(shape.x1, shape.y1), (shape.x2, shape.y2)], fill=shape.outline, width=2)
                    arrowL = 15
                    arrowW = 5
                    dx = shape.x2 - shape.x1
                    dy = shape.y2 - shape.y1
                    length = (dx**2 + dy**2) ** 0.5
                    if length > 0:
                        ux, uy = dx / length, dy / length
                        point1 = (shape.x2, shape.y2)
                        point2 = (shape.x2 - arrowL * ux + arrowW * uy, shape.y2 - arrowL * uy - arrowW * ux)
                        point3 = (shape.x2 - arrowL * ux - arrowW * uy, shape.y2 - arrowL * uy + arrowW * ux)
                        draw.polygon([point1, point2, point3], fill=shape.outline)
                else:
                    draw.rectangle([(shape.x1, shape.y1), (shape.x2, shape.y2)], outline=shape.outline, fill=shape.fill)
        try:
            image.save(filePath)
            messagebox.showinfo("Success", f"Scene successfully saved as PNG: {filePath}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save PNG file: {e}")