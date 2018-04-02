# Running the Project
First of all all dependencies (see README) must be installed.

Thereafter it is just a matter of running modules in the right order.
1. Manager API and Manager
2. Sensor and ParkingLot creator GUIs
3. ParkingLot creation
4. Sensor creation
5. Client Interface

### Manager Creation
To create the Manager and Manager API you must run the python program located in Manager/manager_app.py.

This program initiates a Manager and its REST interface (on port 5000).


### Sensor and ParkingLot GUIs
The GUIs used to test ParkingLot and Sensors can be opened trough the python program UI/\_\_init\_\_.py

The program will open two windows which allow for the creation of ParkingLot and Sensor objects.
### ParkingLot Creation
It is important that ParkingLots are created first. As sensors will be sending updates to these.

Each created parking lot will open a new window showing all relevant information about the parking lot. Here you can also see on which port the parking lot will be listening.

### Sensor Creation
For sensors, it is important to first set the port the on which ParkingLot is listening in the relevant text-field.

Thereafter a sensor window will appear. This window will contain a button which can be used to trigger the state of the sensor and update the parking lot.

### Client Interface