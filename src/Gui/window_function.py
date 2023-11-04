class SetWindowPosition:
    
    def __init__(self,window, position=(0,0,'c')):
        """
        Set the geometry of a window based on a specified position and anchor.

        Args:
            window (Tk or Toplevel): The window for which to set the geometry.
            position (tuple, optional): A tuple specifying the initial position and anchor.
                Default is (0,0,'c').

        Returns:
            None
        """
        window.update_idletasks()  # Actualize geometry
        anchor = position[-1]
        x_anchor = "-" if "w" not in anchor else "+"
        y_anchor = "-" if "n" not in anchor else "+"
        screen_w = window.winfo_screenwidth() // 2
        screen_h = window.winfo_screenheight() // 2

        top_w = window.winfo_width() // 2
        top_h = window.winfo_height() // 2

        if all(["e" not in anchor, "w" not in anchor]):
            xpos = screen_w - top_w
        else:
            xpos = position[0]

        if all(["n" not in anchor, "s" not in anchor]):
            ypos = screen_h - top_h
        else:
            ypos = position[1]

        if 'c' in anchor:  # center of the screen
            xpos = screen_w - top_w
            ypos = screen_h - top_h
        window.geometry(f"{x_anchor}{xpos}{y_anchor}{ypos}")