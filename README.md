# Flask-TensorFlow-AngularJs
An example Neural Network Classifier developed with TensorFlow, Flask (Python framework for server side) and AngularJs + Angular Material (Client side).

Dataset is UrbanSound8K from Justin Salamon, Christopher Jacoby and Juan Pablo Bello.
## Installations (python 2.7):
~~~~
1. virtualenv env
2. source env/bin/activate
3. pip install -r requirements.txt
~~~~

## Start-up:
~~~~
gunicorn main:app
* The server should be started on http://127.0.0.1:8000/
** Work with Chrome, Safari, Firefox.
~~~~
~~~~
python main.py
* The server should be started on http://127.0.0.1:5000/
** Work with Chrome, Firefox only.
~~~~

The app were firstly intent to deploy on Google App Engine.
Install Google App Engine SDK and then
~~~~
gcloud app deploy
~~~~
