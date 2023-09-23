from PIL import Image, ImageDraw, ImageTk
import tkinter as tk
from dataclasses import dataclass
import time, threading

# img_original = Image.new("RGBA", (500, 500), (0, 255, 255, 255))

# img_copy = img_original
# d = ImageDraw.Draw(img_copy)
# # d.regular_polygon((100,100,100),n_sides=3,fill="red",width=0,outline=None)
# d.ellipse(xy=[(0, 0), img_original.size], fill='black')
# img_copy.show()
# # new = Image.alpha_composite(img_original, img_copy)
# # new.show()

# TODO: implement size


class ImgHover(tk.Frame):
    def __init__(self, master, size=None, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)

        self.img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
        self.copy_img = self.img.copy()

        self.img_tk = ImageTk.PhotoImage(self.copy_img)

        self.play = tk.Label(self, text='Img Hover', image=self.img_tk,
                             compound='center', bd=0, highlightthickness=0, relief='ridge')
        self.play.pack()

        self.bind('<Enter>', lambda event : self.threader(self.draw_image))
        self.bind('<Leave>', self.undraw_image)

        self.animate_number = 1

    def threader(self,func,*args):
        threading.Thread(target=func,daemon=True).start()

    def draw_image(self, *args):

        draw = ImageDraw.Draw(self.copy_img)        
        draw.regular_polygon((64, 64, self.animate_number*2), n_sides=3,
                            fill="#2c232c", width=0, outline=None, rotation=-90)
        self.copy_img_tk = ImageTk.PhotoImage(self.copy_img)
        self.play.configure(image=self.copy_img_tk)

        print(self.animate_number,end = '\r')

        if self.animate_number < 32:
            self.after(1,self.draw_image)
            self.animate_number += 1
        else:
            self.animate_number = 1
            self.copy_img = self.img.copy()
            
        
            

    def undraw_image(self, *args):
        self.play.configure(image=self.img_tk)


@dataclass
class ImgParameters:
    width: int = 128
    height: int = 128

    # methods
    def to_point(self, start_at: tuple = (0, 0)):
        new_width = start_at[0]+self.width
        new_height = start_at[1]+self.height
        return [(start_at[0], start_at[1]), (new_width, new_height)]


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('500x500')
    root.configure(bg='red')
    ImgHover(master=root).pack(padx=10, pady=10)

    root.mainloop()
