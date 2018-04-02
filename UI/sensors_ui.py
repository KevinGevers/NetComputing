from tkinter import *
from ParkingLot.sensor import Sensor, SensorStatus


SENSOR_ID = 1

HOST = '127.0.0.1'
PORT = 6606


class SensorUI(Frame):

    def __init__(self, port, master=None):
        Frame.__init__(self, master)
        self.pack()

        global SENSOR_ID
        self.sensor = Sensor(SENSOR_ID, HOST, port)
        self.sensor.update()
        SENSOR_ID += 1

        self.create_widgets()

    def create_widgets(self):
        self.tag = Label(self)
        self.tag['text'] = self.sensor.uid
        self.tag.pack(side="top")

        self.btn_sensor = Button(self)
        self.btn_sensor.pack(side="bottom")
        self.btn_sensor["command"] = self.trigger_sensor

        self.update_btn_tag()

    def update_btn_tag(self):
        tag = 'Taken'
        if self.sensor.status == SensorStatus.AVAILABLE:
            tag = 'Available'

        self.btn_sensor['text'] = tag

    def trigger_sensor(self):
        self.sensor.trigger()
        self.update_btn_tag()


class SensorCreator(Frame):
    sensors = set()

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.input_tag = Label(self, text='Port')
        self.input_tag.pack()
        self.input_port = Entry(self, width=10, textvariable=StringVar(self.master, value='6606'))
        self.input_port.pack()

        self.btn_create = Button(self)
        self.btn_create["text"] = "ADD SENSOR"
        self.btn_create["command"] = self.new_sensor
        self.btn_create.pack()

        self.QUIT = Button(self, text="CLOSE ALL", fg="red", command=self.close_all)
        self.QUIT.pack(side="bottom")

    def close_all(self):
        for c in self.sensors:
            c.destroy()
        self.master.destroy()

    def get_port(self):
        try:
            return int(self.input_port.get())
        except ValueError:
            return 6606

    def new_sensor(self):
        root = Tk()
        self.sensors.add(root)
        sensor = SensorUI(self.get_port(), master=root)
        sensor.mainloop()