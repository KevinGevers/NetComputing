from tkinter import *
from ParkingLot.sensor import Sensor, SensorStatus

HOST = '127.0.0.1'
PORT = 6606

class SensorUI(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.sensor = Sensor(HOST, PORT)

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
        self.btn_create = Button(self)
        self.btn_create["text"] = "ADD SENSOR"
        self.btn_create["command"] = self.new_sensor
        self.btn_create.pack(side="top")

        self.QUIT = Button(self, text="CLOSE ALL", fg="red",
                                            command=self.close_all)
        self.QUIT.pack(side="bottom")

    def close_all(self):
        for c in self.sensors:
            c.destroy()
        root.destroy()

    def new_sensor(self):
        root = Tk()
        self.sensors.add(root)
        sensor = SensorUI(master=root)
        sensor.mainloop()


root = Tk()
app = SensorCreator(master=root)
app.mainloop()