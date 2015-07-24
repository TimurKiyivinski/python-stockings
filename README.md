python-stockings
================
A simple Python library containing an example socket server and class.

usage
=====
Add `stockings` into your development directory and import it with `import stockings`.

demo
====
Run the server.
```
python3 _server.py
```
Run the listener application.
```
python3 _client.py
```
Run the user application. 
```
python3 _user.py
```
Type any random input into the user application. The data is sent as a `pickled` class to the server and from there to the client. The client unpacks the data and uses a function to process the length of the encapsulated message.
