import tkinter as tk
from screens import preview_screen
from pystray import MenuItem as item
import pystray
from PIL import Image


def quit_window(icon):
    icon.stop()
    window.destroy()


def show_window(icon):
    icon.stop()
    window.after(0, window.deiconify)


def withdraw_window():
    window.withdraw()
    image = Image.open("image.ico")
    menu = (item('Выйти из приложения', quit_window), item('Открыть приложение', show_window))
    icon = pystray.Icon("name", image, "title", menu)
    icon.run()


class App(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        preview_screen.start(window)
        #window.update()
    def refresh(self):
        print('yes')
        self.destroy()
        self.__init__(window)


window = tk.Tk()
window.resizable(width=False, height=False)
app = App(window)
window.title("VK Manager")
window.configure(bg="#B0C4DE")
w, h = 800, 600
window.geometry("%dx%d+0+0" % (w, h))
#  Screen One

#
window.protocol('WM_DELETE_WINDOW', withdraw_window)
window.mainloop()