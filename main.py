from tkinter import Tk
from product import Product


if __name__ == "__main__":
    window = Tk()
    application = Product(window)
    window.mainloop()