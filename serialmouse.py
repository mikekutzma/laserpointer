from tkinter import Tk, Label, Button
import serial
from time import sleep

ser = serial.Serial('/dev/ttyACM1',9600)
class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("A simple GUI")

        self.label = Label(master, text="This is our first GUI!")
        self.label.pack()

        self.greet_button = Button(master, text="Greet", command=self.greet)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def greet(self):
        print("Greetings!")

def motion(event):
    x, y = event.x, event.y
    outstring = str(x)+';'+str(y)
    print(outstring)
    ser.write(bytes(outstring,'utf-8'))
    sleep(0.05)

root = Tk()
root.bind('<Motion>',motion)
my_gui = MyFirstGUI(root)
root.mainloop()
