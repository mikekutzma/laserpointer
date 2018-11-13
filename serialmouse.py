from tkinter import Tk, Label, Button
import serial
from time import sleep

FACT = 4
MAXVAL = 160

ser = serial.Serial('/dev/ttyACM0',9600)
class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("SerialMouse")

        self.label = Label(master, text="Mouse control")
        self.label.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

def motion(event):
    x, y = event.x, event.y
    x = MAXVAL - int(x/FACT)
    y = MAXVAL - int(y/FACT)
    outstring = '<'+str(x)+','+str(y)+'>'
    print(outstring)
    ser.write(outstring.encode('utf-8'))
    sleep(0.1)

root = Tk()
root.geometry("{}x{}".format(160*FACT,160*FACT))
root.bind('<Motion>',motion)
my_gui = MyFirstGUI(root)
root.mainloop()
