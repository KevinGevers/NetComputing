from tkinter import *
from ParkingLot.parking_lot import ParkingLot
import _thread

PARK_ID = 1
PORT = 6605

HEADER_TAG = 'Parking ID: {0}\nRunning on port: {1}\n'

class ParkingUI(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()

        global PARK_ID
        parking_id = PARK_ID
        self.parking = ParkingLot(parking_id, PORT+PARK_ID)
        self.parking.set_manager('localhost')
        PARK_ID += 1

        self.create_widgets()

    def create_widgets(self):
        self.p_id = Label(self)
        self.p_id['text'] = HEADER_TAG.format(self.parking.uid, self.parking.port)
        self.p_id.pack(side="top")

        self.sensors = Label(self)
        self.sensors.pack(side="top")
        self.taken = Label(self)
        self.taken.pack(side="top")

        self.update_tags()

        _thread.start_new_thread(self.parking.start_server, ())

    def update_tags(self):
        self.sensors['text'] = "Number of sensors: " + str(len(self.parking.sensors))
        self.taken['text'] = "Number of reserved spots: " + str(len(self.parking.taken))

        self.master.after(1000, self.update_tags)



class ParkingCreator(Frame):
    sensors = set()

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.input_tag = Label(self, text='Port')
        self.input_tag.pack()
        self.input_port = Entry(self, width=10, textvariable=StringVar(self.master, value='5000'))
        self.input_port.pack()

        self.btn_create = Button(self)
        self.btn_create["text"] = "ADD PARKING LOT"
        self.btn_create["command"] = self.new_sensor
        self.btn_create.pack(side="top")

        self.QUIT = Button(self, text="CLOSE ALL", fg="red",
                                            command=self.close_all)
        self.QUIT.pack(side="bottom")

    def close_all(self):
        for c in self.sensors:
            c.destroy()
        self.master.destroy()

    def new_sensor(self):
        root = Tk()
        self.sensors.add(root)
        sensor = ParkingUI(master=root)
        sensor.mainloop()
