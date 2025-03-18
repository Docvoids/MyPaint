import tkinter as tk

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltipWindow = None
        # Bind mouse events to the widget
        self.widget.bind("<Enter>", self.showTooltip)
        self.widget.bind("<Leave>", self.hideTooltip)

    def showTooltip(self, event=None):
        if self.tooltipWindow or not self.text:
            return
        # Create a new window for the tooltip
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 20
        y += self.widget.winfo_rooty() + 10
        self.tooltipWindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # Disable standard window
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,background="#ffffe0", relief=tk.SOLID, borderwidth=1,font=("tahoma", "8", "normal"))
        label.pack(ipadx=5, ipady=2)

    def hideTooltip(self, event=None):
        if self.tooltipWindow:
            self.tooltipWindow.destroy()
            self.tooltipWindow = None