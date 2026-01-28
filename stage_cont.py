# -*- coding: utf-8 -*-
"""
Python GUI Application using Tkinter for controlling a device via serial communication
First edit by K.Kawade
29 Aug 2024
"""

import serial
import tkinter as tk
import time
import sys

class StageController:
    def __init__(self, root):
        # Initialize the serial port to None
        self.ser = None
        
        # Set up the GUI
        self.root = root
        self.root.title("Stage Controller for SIGMA-KOKI SHOT-204")
        self.root.geometry("640x420")
        
        self.create_widgets()

    def create_widgets(self):
        # Declare Buttons
        # Buttons with fixed width
        button_width = 7

        self.button_connect  = tk.Button(self.root, text='Connect',   command=self.click_Comm,    width=button_width)
        self.button_origin   = tk.Button(self.root, text='Origin',    command=self.click_Origin,  width=button_width)
        self.button_move_rel = tk.Button(self.root, text='Move(Rel)', command=self.click_MoveRel, width=button_width)
        self.button_move_abs = tk.Button(self.root, text='Move(Abs)', command=self.click_MoveAbs, width=button_width)
        self.button_speed    = tk.Button(self.root, text='Speed',     command=self.click_Speed,   width=button_width)
        self.button_jog      = tk.Button(self.root, text='JOG',       command=self.click_JOG,     width=button_width)
        self.button_stop     = tk.Button(self.root, text='Stop',      command=self.click_Stop,    width=button_width)
        self.button_position = tk.Button(self.root, text='Position',  command=self.click_Status,  width=button_width)
        self.button_exit     = tk.Button(self.root, text='Exit',      command=self.click_Exit,    width=button_width)
        
        # Place buttons
        self.button_connect.place( x=100, y=10)
        self.button_origin.place(  x=100, y=80)
        self.button_move_rel.place(x=100, y=120)
        self.button_move_abs.place(x=100, y=160)
        self.button_speed.place(   x=100, y=200)
        self.button_jog.place(     x=100, y=240)
        self.button_stop.place(    x=100, y=280)
        self.button_position.place(x=100, y=320)
        self.button_exit.place(    x=100, y=360)

        # Labels
        self.lbl    = tk.Label(text='---------')
        self.lbSlow = tk.Label(text='S')
        self.lbFast = tk.Label(text='F')
        self.lbRate = tk.Label(text='R')
        self.lbl.place(   x=200, y=320)
        self.lbSlow.place(x=200, y=200)
        self.lbFast.place(x=290, y=200)
        self.lbRate.place(x=380, y=200)

        # Textboxes
        self.txt1    = tk.Entry(width=10)
        self.txt2    = tk.Entry(width=10)
        self.txtSlow = tk.Entry(width=10)
        self.txtFast = tk.Entry(width=10)
        self.txtRate = tk.Entry(width=10)
        
        # Place textboxes
        self.txt1.place(   x=200, y=120)
        self.txt2.place(   x=200, y=160)
        self.txtSlow.place(x=200, y=200)
        self.txtFast.place(x=290, y=200)
        self.txtRate.place(x=380, y=200)

        # Default values
        self.txt1.insert(   tk.END, "100")
        self.txt2.insert(   tk.END, "0")
        self.txtSlow.insert(tk.END, "2000")
        self.txtFast.insert(tk.END, "20000")
        self.txtRate.insert(tk.END, "200")

        # Radiobuttons for axis selection
        self.var = tk.IntVar()
        self.rdo1 = tk.Radiobutton(value=1, variable=self.var, text='Axis1')
        self.rdo2 = tk.Radiobutton(value=2, variable=self.var, text='Axis2')
        self.rdo3 = tk.Radiobutton(value=3, variable=self.var, text='Axis3')
        self.rdo4 = tk.Radiobutton(value=4, variable=self.var, text='Axis4')
        self.rdo5 = tk.Radiobutton(value=0, variable=self.var, text='All')
        self.rdo1.place(x=100, y=50)
        self.rdo2.place(x=160, y=50)
        self.rdo3.place(x=220, y=50)
        self.rdo4.place(x=280, y=50)
        self.rdo5.place(x=340, y=50)
        self.var.set(1)

        # Radiobuttons for direction selection
        self.var2 = tk.IntVar()
        self.rdoP = tk.Radiobutton(value=1, variable=self.var2, text='+')
        self.rdoM = tk.Radiobutton(value=2, variable=self.var2, text='-')
        self.rdoP.place(x=200, y=240)
        self.rdoM.place(x=240, y=240)
        self.var2.set(1)

    def click_Comm(self):
        """Establish serial communication."""
        self.ser = serial.Serial('COM3') # Check device manager
        self.ser.baudrate = 38400
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.timeout = 5
        self.ser.rtscts = True

    def click_Origin(self):
        """Send the origin command to the selected axis."""
        if self.ser is None:
            return
        axis = 'W' if self.var.get() == 0 else str(self.var.get())
        wdata = f'H:{axis}\r\n'
        print(wdata)
        self.ser.write(wdata.encode())
        rdata = self.ser.readline()
        print(rdata)

    def click_MoveRel(self):
        """Move the selected axis to a relative position."""
        if self.ser is None:
            return
        sss = self.txt1.get()
        if not sss.isdigit():
            return
        direction = '+' if int(sss) > 0 else '-'
        axis = 'W' if self.var.get() == 0 else str(self.var.get())
        wdata = f'M:{axis}{direction}P{sss}\r\n'
        print(wdata)
        self.ser.write(wdata.encode())
        rdata = self.ser.readline()
        print(rdata)

        time.sleep(1)
        wdata = 'G:\r\n'
        print(wdata)
        self.ser.write(wdata.encode())
        rtn = self.ser.readline()
        print(rtn)

    def click_MoveAbs(self):
        """Move the selected axis to an absolute position."""
        if self.ser is None:
            return
        sss = self.txt2.get()
        if not sss.isdigit():
            return
        direction = '+' if int(sss) > 0 else '-'
        axis = 'W' if self.var.get() == 0 else str(self.var.get())
        wdata = f'A:{axis}{direction}P{sss}\r\n'
        print(wdata)
        self.ser.write(wdata.encode())
        rdata = self.ser.readline()
        print(rdata)

        time.sleep(1)
        wdata = 'G:\r\n'
        print(wdata)
        self.ser.write(wdata.encode())
        rtn = self.ser.readline()
        print(rtn)

    def click_Speed(self):
        """Set the speed of the selected axis."""
        if self.ser is None:
            return
        slow = self.txtSlow.get()
        if not slow.isdigit():
            return
        fast = self.txtFast.get()
        if not fast.isdigit():
            return
        rate = self.txtRate.get()
        if not rate.isdigit():
            return
        axis = 'W' if self.var.get() == 0 else str(self.var.get())
        wdata = f'D:{axis}S{slow}F{fast}R{rate}\r\n'
        print(wdata)
        self.ser.write(wdata.encode())
        rdata = self.ser.readline()
        print(rdata)

    def click_JOG(self):
        """Jog the selected axis."""
        if self.ser is None:
            return
        direction = '+' if self.var2.get() == 1 else '-'
        axis = 'W' if self.var.get() == 0 else str(self.var.get())
        wdata = f'J:{axis}{direction}\r\n'
        print(wdata)
        self.ser.write(wdata.encode())
        rdata = self.ser.readline()
        print(rdata)

        time.sleep(1)
        wdata = 'G:\r\n'
        print(wdata)
        self.ser.write(wdata.encode())
        rtn = self.ser.readline()
        print(rtn)

    def click_Stop(self):
        """Stop the selected axis."""
        if self.ser is None:
            return
        axis = 'W' if self.var.get() == 0 else str(self.var.get())
        wdata = f'L:{axis}\r\n'
        print(wdata)
        self.ser.write(wdata.encode())
        rdata = self.ser.readline()
        print(rdata)

    def click_Status(self):
        """Check the status of the selected axis."""
        if self.ser is None:
            return
        wdata = 'Q:\r\n'
        print(wdata)
        self.ser.write(wdata.encode())
        rdata = self.ser.readline()
        print(rdata)
        if self.var.get() == 0:
            sss = rdata[0:21]
        elif self.var.get() == 1:
            sss = rdata[0:10]
        else:
            sss = rdata[12:21]
        self.lbl['text'] = sss
    
    def click_Exit(self):
        if self.ser:
            self.ser.close()
        time.sleep(1)
        root.destroy()
        sys.exit()
    
    def send_command(self, command):
        print(command)
        self.ser.write(command.encode())
        rdata = self.ser.readline()
        print(rdata)

if __name__ == "__main__":
    root = tk.Tk()
    app = StageController(root)
    root.mainloop()
