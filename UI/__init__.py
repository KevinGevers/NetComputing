from UI.parking_ui import ParkingCreator
from UI.sensors_ui import SensorCreator
from tkinter import Tk
import _thread
import time

running = 0

def start_parking():
    global running
    running += 1

    root1 = Tk()
    app1 = ParkingCreator(master=root1)
    app1.mainloop()

    running -= 1

def start_sensor():
    global running
    running += 1

    root2 = Tk()
    app2 = SensorCreator(master=root2)
    app2.mainloop()

    running -= 1


if __name__ == "__main__":
    _thread.start_new_thread(start_parking, ())
    time.sleep(1)
    _thread.start_new_thread(start_sensor, ())

    time.sleep(1)

    while running > 0:
        time.sleep(2)