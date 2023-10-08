from PIL import Image, ImageDraw, ImageTk, ImageEnhance, ImageChops
import tkinter as tk
# from src.Gui.components import CanvasWithParentBackground
from tkinter import Canvas
from dataclasses import dataclass
import os
import threading
import time


def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.2f} seconds to execute.")
        return result
    return wrapper


@dataclass(frozen=True)
class MyImage:
    width: int = None
    height: int = None

    def bounding_box(self, offset=(0, 0)):
        """
        Calculate the bounding box coordinates.

        Args:
            offset (tuple, optional): Offset for the bounding box. Default is (0, 0).

        Returns:
            list: List of bounding box coordinates [(x0, y0), (x1, y1)].
        """
        x0y0 = offset  # Default (0,0)
        x1y1 = (offset[0] + self.width, offset[1] + self.height)
        return [x0y0, x1y1]

    def largest_inscribed_circle(self, list_of_point_pair):
        """
        Calculate the parameters of the largest inscribed circle within a bounding box.

        Args:
            list_of_point_pair (list): List of two points [(x0, y0), (x1, y1)] representing a bounding box.

        Returns:
            tuple: A tuple containing the center coordinates ((center_x, center_y)) and the radius of the circle.
        """
        # Calculate the width and height of the bounding box
        point1, point2 = list_of_point_pair
        width = abs(point2[0] - point1[0])
        height = abs(point2[1] - point1[1])

        # Calculate the radius (half of the smaller dimension)
        radius = min(width, height) / 2

        # Calculate the center of the circle
        center_x = point1[0] + width / 2
        center_y = point1[1] + height / 2

        return ((center_x, center_y), radius)

    def create_empty(self, width=None, height=None, color='#00000000'):
        """
        Create a transparent image.

        Args:
            color (str, optional): Background color of the image in RGBA format. Default is fully transparent.

        Returns:
            Image: A transparent image with the specified width and height.
        """
        if width is None and height is None:
            width = self.width
            height = self.height

        return Image.new("RGBA", (width, height), color)

    def create(self, shape='circle', offset=(0, 0), **kwargs):
        """
        Create an image with the specified shape and attributes.

        Args:
            shape (str): The shape of the image ('circle', 'regular_polygon', 'rounded_rectangle').
            offset (tuple, optional): Offset for the shape. Default is (0, 0).
            **kwargs: Additional keyword arguments to customize the shape.

        Returns:
            Image: An image with the specified shape and attributes.
        """
        base_img = self.create_empty()  # Getting a transparent image
        bounding_box = self.bounding_box(offset)
        draw = ImageDraw.Draw(base_img)

        if shape == "circle":
            draw.ellipse(bounding_box, **kwargs)
        elif shape == "regular_polygon":
            bounding_circle = self.largest_inscribed_circle(bounding_box)
            draw.regular_polygon(bounding_circle, **kwargs)
        elif shape == "rounded_rectangle":
            draw.rounded_rectangle(bounding_box, **kwargs)

        else:

            raise ValueError("Shape doesn't exist")

        return base_img

    def open_image(self, path):
        """
        Open an image file from the specified path.

        Args:
            path (str): The path to the image file.

        Returns:
            Image: The opened image.
        """
        return Image.open(path)

    def resize_image(self, path, width=None, height=None, preserve_aspect=True, resize_percent_of_original=100):
        """
        Resize an image for use as an icon.

        Args:
            path (str): The path to the image file.
            width (int, optional): The target width for resizing. Default is None.
            height (int, optional): The target height for resizing. Default is None.
            resize_percent_of_original (int, optional): The percentage of resizing. Default is 10%.

        Returns:
            Image: The resized image.
        """
        if width is None:
            width = self.width * resize_percent_of_original / 100
        if height is None:
            height = self.height * resize_percent_of_original / 100

        width = width * resize_percent_of_original / 100
        height = height * resize_percent_of_original / 100
        original_image = self.open_image(path)
        if preserve_aspect:
            copy_img = original_image.copy()
            copy_img.thumbnail(
                (width, height), resample=Image.Resampling.LANCZOS)
            return copy_img
        else:
            resized_img = original_image.resize(
                (width, height), resample=Image.Resampling.LANCZOS)
            return resized_img

    @staticmethod
    def to_tk(Image):
        return ImageTk.PhotoImage(Image)


class CanvasWithShape(Canvas):
    def __init__(self, master, shape='rounded_rectangle', width=None, height=None, **kwargs):
        '''
        when height and width are not given instances cannot access the tags as .bind doesn't return anything
        '''

        super().__init__(master=master)

        self.width = width
        self.height = height
        self.shape = shape
        self.kwargs = kwargs

        if width is None and height is None:
            # doesn't return anything
            self.bind('<Configure>', self.create_shape)
        else:

            self.create_shape()

    # @timing_decorator
    def create_shape(self, event=None):
        # not using .winfo_width because sometimes it works and sometimes it doesn't.
        # -> I don't know how to use it properly
        if event:
            # removing any widgets or canvas present before creating them again.
            self.delete('all')
            for slave in self.pack_slaves():
                slave.destroy()

            self.width = event.width
            self.height = event.height

        self.my_image = MyImage(width=self.width, height=self.height)
        self.background_img = self.my_image.create(
            self.shape, **self.kwargs)

        self.copied_original_imag = self.background_img.copy()
        self.background_img_tk = ImageTk.PhotoImage(self.background_img)

        self.create_image(self.width / 2, self.height / 2,
                          image=self.background_img_tk, tags=('background'))

        self.description_heading_frame = tk.Frame(
            master=self,
            # background = self.color,
        )
        self.description_heading_frame.pack(
            fill='x',  pady=(10, 0))

        # Advantages
        description_heading = tk.Label(foreground='Black',
                                       master=self.description_heading_frame,
                                       #    background=,
                                       text="Advantages")
        description_heading.pack(side='left', anchor='nw',  padx=5)

        # i Icon
        i_icon_label = tk.Label(
            master=self.description_heading_frame, text='i')
        i_icon_label.pack(side='right', anchor='ne')

        # # # TExt area
        # text_frame = tk.Frame(master=self,background='pink')
        # text_frame.pack(expand=True,fill='both')
        # sample text
        text = """
Burns calories and fat
Strengthens muscles and bones
Improves posture and balance
Enhances cardiovascular health
Prevents injuries and pain"""

        bullet_points = "• " + "\n• ".join(text.strip().split('\n'))

        # tk.Text(self,width= 200, height=150,background='red').pack()

        text_str = 'sonme text with bullet point \n this is second line'

        text_item = self.create_text(self.width/2, self.height/2, text=bullet_points,
                                     width=self.width, anchor=tk.CENTER, font=('roboto', 12), state=tk.DISABLED)


class CircleImgIcon(Canvas):
    def __init__(self, master, width=None, height=None, fg_img_path='',

                 animate=True, *args, **kwargs):
        super().__init__(master=master,
                         width=width, height=height,
                        #  background='yellow',
                         *args, **kwargs)

        self.fg_img_path = fg_img_path
        self.width = None
        self.height = None
        self.animate = animate

        if width is None and height is None:
            self.bind('<Configure>', self.create_bg_and_fg)
        else:
            self.width = width
            self.height = height
            self.create_bg_and_fg()

    # @timing_decorator
    def create_bg_and_fg(self, event=None):
        if event:
            self.width = event.width
            self.height = event.height
            self.delete('all')  # clear previous images on canvas if present

        self.my_image = MyImage(width=self.width, height=self.height)

        # Creating background
        self.background_img = self.my_image.create(
            shape='circle', fill=(204, 242, 255, 170), width=0)

        self.copied_original_imag = self.background_img.copy()
        self.background_img_tk = ImageTk.PhotoImage(self.background_img)

        self.create_image(self.width / 2, self.height / 2,
                          image=self.background_img_tk, tag='background')

        # Foreground image
        if os.path.exists(self.fg_img_path):
            self.resized_foreground_img = self.my_image.resize_image(
                self.fg_img_path, resize_percent_of_original=90)
        else:
            print('The file does not exist')
            # Todo: Add handling for cases when the file doesn't exist (e.g., display a placeholder)

        self.resized_foreground_tk = ImageTk.PhotoImage(
            self.resized_foreground_img)
        self.create_image(self.width / 2, self.height / 2,
                          image=self.resized_foreground_tk, tag='foreground')

        # Event handlers
        if self.animate:
            self.bind('<Enter>', lambda event: self.threader(self.change_color))
            self.bind('<Leave>', lambda event: self.threader(
                self.revert_to_original_state))

        self.animate_number = 1  # Counter (may need improvement)

    def threader(self, func, *args):
        """Start a new thread to execute a function."""
        # print('Threading...', func.__name__)
        threading.Thread(target=func, daemon=True).start()

    # @timing_decorator
    def change_color(self):
        """Change the color of the background shape on hover."""
        enhancer = ImageEnhance.Brightness(self.background_img)
        enhanced_img = enhancer.enhance(.8)
        # self.move('background', 10, 0)

        self.enhanced_img_tk = ImageTk.PhotoImage(enhanced_img)
        self.itemconfig('background', image=self.enhanced_img_tk)
        self.tag_raise('foreground')

    def revert_to_original_state(self, *args):
        """Undraw the image."""

        self.itemconfig('background', image=self.background_img_tk)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('500x500')
    root.configure(background='white')
    frame = tk.Frame(root, background='yellow')
    frame.pack(expand=True, fill='both')
    circle_icon = CircleImgIcon(master=frame,
                                # width=128, height=128,
                                fg_img_path=r'C:\Scripts\01_PYTHON\Projects\Workout_Reminder\resources\icons\dumbell.png')

    circle_icon.pack(padx=10, pady=10,
                     expand=True, fill='both'
                     )
    # CanvasWithShape(root, shape='rounded_rectangle', fill=(104, 0, 255, 30), radius=15).pack(padx=10, pady=10,
    #                                                                                          expand=True, fill='both'
    #                                                                                          )

    root.mainloop()
