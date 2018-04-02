
# NetComputing Group 5
## Instalation requirements
The project was created using python 3.5.

### Python dependencies
Our project uses the following dependencies which can be installed trough pip:
* flask
* pika

### RabbitMQ
Download [RabbitMQ](https://www.rabbitmq.com/) and it's dependencies from the link.

## API descriptions
### Manager

The resources are reservation and the reservation are the following JSON objects:
```json
[reservation] = {
    'client_id' = [string],
    'start_time' = [number],
    'end_time' = [number]
}
```

`http://[hostname]/parkingspaces`: With the GET method the client can retrieve the total parking spaces, the number of open parking spaces and the number of reserved parking spaces. The information will be given in the following JSON format:
```json
'total' = [number],
'available' = [number],
'reservations' = [number]
```

'http://[hostname]/reservations': With the GET method the user can retrieve the list of reservations from the manager.

`http://[hostname]/reservations`: With the POST method the user can create a new reservation if successful it will return your reservation in the following JSON format:
```json
'reservation' = [reservation]
```
The following variables have to be attached to the request:
```json
'id' = [string]
```
The following error codes can occur during the POST request:
* Error 400: If the request does not use the correct variables.
* Error 404: If a reservation already exists for that id.
* If there is no space available for the reservation it will send an empty object with the code 204.

`http://[hostname]/reservations/[client_id]`: With the GET method the user can retrieve the reservation with the id {[}client\_id{]}. The reservation will be given in the following format:
```json
'reservation' = [reservation]
```
If the reservation does not exist then it will return the error 404.

`http://[hostname]/reservations/[client_id]`: With the DELETE method the user can delete the reservation with the id {[}client\_id{]}. If the request succeeds it will return the reservation in the following format:
```json
'result'= [Boolean]],
'reservation' = [reservation]
```
If the reservation does not exit it will return the error 404.

### Server
The manager resource follows the following format:
```json
[manager] = {
    'id'= [number],
    'manager_url' = [string]
    'manager_location_latitude' = [string]
    'manager_location_longitude' = [string]
}
```

`http://[hostname]/managers`: With the GET method the user can retrieve a list of managers. In the following format:
```json
'managers' = [
    [manager],
    ...
]
```

`http://[hostname]/managers`: With the POST method the user can create a new manager. When successful it will return code 201 and the following data:
```json
'manager' = [manager]
```
The POST data has to follow the following format:
```json
'manager_url' = [string]
'manager_location_latitude' = [string]
'manager_location_longitude' = [string]
```
If the data given in the wrong format the request will return a 400 error.

`http://[hostname]/managers/[manager_url]`: With the DELETE method the user can delete the manager from the server.