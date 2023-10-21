import tkinter as tk
from tkinter import ttk
s = ttk.Style()
object = ttk.Listbox(None)

object_class = object.winfo_class()
print(s.layout(object_class))