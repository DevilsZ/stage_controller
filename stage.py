# -*- coding: utf-8 -*-
"""
Tkinter GUI for SIGMA-KOKI SHOT-204
Refactored with separated serial communication class
"""

import tkinter as tk
import serial
import sys


# =========================
# Serial Communication Class
# =========================
class SerialController:
    def __init__(self):
        self.ser = None

    def open(self, port):
        try:
            self.ser = serial.Serial(
                port=port,
                baudrate=38400,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=2,
                rtscts=True
            )
            return True
        except serial.SerialException as e:
            print(f"Serial open error: {e}")
            self.ser = None
            return False

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()

    def is_open(self):
        return self.ser is not None and self.ser.is_open

    def send(self, command):
        """Send command and read response"""
        if not self.is_open():
            return None

        try:
            self.ser.write(command.encode())
            rdata = self.ser.readline()
            return rdata.decode(errors="ignore").strip()
        except serial.SerialException as e:
            print(f"Serial communication error: {e}")
            return None


# =========================
# GUI Controller Class
# =========================
class StageController:
    def __init__(self, root):
        self.root = root
        self.root.title("Stage Controller for SIGMA-KOKI SHOT-204")
        self.root.geometry("640x420")

        self.serial = SerialController()
        self.create_widgets()

    # ---------- GUI ----------
    def create_widgets(self):
        button_width = 7

        tk.Button(self.root, text='Connect',   command=self.click_connect,   width=button_width).place(x=100, y=10)
        tk.Button(self.root, text='Origin',    command=self.click_origin,    width=button_width).place(x=100, y=80)
        tk.Button(self.root, text='Move(Rel)', command=self.click_move_rel,  width=button_width).place(x=100, y=120)
        tk.Button(self.root, text='Move(Abs)', command=self.click_move_abs,  width=button_width).place(x=100, y=160)
        tk.Button(self.root, text='Speed',     command=self.click_speed,     width=button_width).place(x=100, y=200)
        tk.Button(self.root, text='JOG',       command=self.click_jog,       width=button_width).place(x=100, y=240)
        tk.Button(self.root, text='Stop',      command=self.click_stop,      width=button_width).place(x=100, y=280)
        tk.Button(self.root, text='Position',  command=self.click_status,    width=button_width).place(x=100, y=320)
        tk.Button(self.root, text='Exit',      command=self.click_exit,      width=button_width).place(x=100, y=360)

        self.lbl_status = tk.Label(self.root, text='---------')
        self.lbl_status.place(x=200, y=320)

        self.txt_usb  = tk.Entry(self.root, width=20)
        self.txt_rel  = tk.Entry(self.root, width=10)
        self.txt_abs  = tk.Entry(self.root, width=10)
        self.txtSlow  = tk.Entry(self.root, width=10)
        self.txtFast  = tk.Entry(self.root, width=10)
        self.txtRate  = tk.Entry(self.root, width=10)

        self.txt_usb.place(x=200, y=10)
        self.txt_rel.place(x=200, y=120)
        self.txt_abs.place(x=200, y=160)
        self.txtSlow.place(x=200, y=200)
        self.txtFast.place(x=290, y=200)
        self.txtRate.place(x=380, y=200)

        self.txt_usb.insert(0, "/dev/ttyUSB0")
        self.txt_rel.insert(0, "100")
        self.txt_abs.insert(0, "0")
        self.txtSlow.insert(0, "2000")
        self.txtFast.insert(0, "20000")
        self.txtRate.insert(0, "200")

        self.axis = tk.IntVar(value=1)
        for i, label in enumerate(["Axis1", "Axis2", "Axis3", "Axis4", "All"]):
            value = 0 if label == "All" else i + 1
            tk.Radiobutton(self.root, text=label, variable=self.axis, value=value).place(x=100 + 60*i, y=50)

        self.direction = tk.IntVar(value=1)
        tk.Radiobutton(self.root, text='+', variable=self.direction, value=1).place(x=200, y=240)
        tk.Radiobutton(self.root, text='-', variable=self.direction, value=2).place(x=240, y=240)

    # ---------- Utility ----------
    def get_axis(self):
        return 'W' if self.axis.get() == 0 else str(self.axis.get())

    def safe_int(self, text):
        try:
            return int(text)
        except ValueError:
            return None

    # ---------- Button Handlers ----------
    def click_connect(self):
        if self.serial.open('COM3'):   # Linux: /dev/ttyUSB0 等
            print("Serial connected")

    def click_origin(self):
        cmd = f'H:{self.get_axis()}\r\n'
        print(self.serial.send(cmd))

    def click_move_rel(self):
        value = self.safe_int(self.txt_rel.get())
        if value is None:
            return
        direction = '+' if value >= 0 else '-'
        cmd = f'M:{self.get_axis()}{direction}P{abs(value)}\r\n'
        print(self.serial.send(cmd))
        self.root.after(500, lambda: print(self.serial.send('G:\r\n')))

    def click_move_abs(self):
        value = self.safe_int(self.txt_abs.get())
        if value is None:
            return
        cmd = f'A:{self.get_axis()}P{value}\r\n'
        print(self.serial.send(cmd))
        self.root.after(500, lambda: print(self.serial.send('G:\r\n')))

    def click_speed(self):
        slow = self.safe_int(self.txtSlow.get())
        fast = self.safe_int(self.txtFast.get())
        rate = self.safe_int(self.txtRate.get())
        if None in (slow, fast, rate):
            return
        cmd = f'D:{self.get_axis()}S{slow}F{fast}R{rate}\r\n'
        print(self.serial.send(cmd))

    def click_jog(self):
        direction = '+' if self.direction.get() == 1 else '-'
        cmd = f'J:{self.get_axis()}{direction}\r\n'
        print(self.serial.send(cmd))
        self.root.after(500, lambda: print(self.serial.send('G:\r\n')))

    def click_stop(self):
        cmd = f'L:{self.get_axis()}\r\n'
        print(self.serial.send(cmd))

    def click_status(self):
        resp = self.serial.send('Q:\r\n')
        if resp:
            self.lbl_status['text'] = resp

    def click_exit(self):
        self.serial.close()
        self.root.destroy()
        sys.exit()


# =========================
# Main
# =========================
if __name__ == "__main__":
    root = tk.Tk()
    app = StageController(root)
    root.mainloop()
