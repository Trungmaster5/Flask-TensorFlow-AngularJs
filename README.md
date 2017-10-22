# Flask-TensorFlow-AngularJs
An example Neural Network Classifier developed with TensorFlow, Flask (Python framework for server side) and AngularJs + Angular Material (Client side).

## Installations (python 2.7):
~~~~
1. virtualenv env
2. source env/bin/activate
3. pip install -r requirements.txt
~~~~

## Start-up:
~~~~
python main.py
~~~~

The server should be started on http://127.0.0.1:5000/

## Limitations:
The app were firstly intented to deploy on Google App Engine. The deployment is not yet possible at the present time (10/2017), because GAE only support numpy 1.6.x while the app requires numpy above 1.9.x.  
