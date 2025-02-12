import tkinter as tk
from gui import OBDApp

if __name__ == "__main__":
    root = tk.Tk()
    app = OBDApp(root)
    root.mainloop()