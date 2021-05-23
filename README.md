# IVI
Intelligent Visual identifier for reviewing pdf docs and highlights changes.
# Installation 

After cloning the repo, follow the below steps to run the application -

# Frontend

$ cd ivi-frontend/ <br />
$ npm install <br />
$ npm start <br />

This should start the react frontend dev server on localhost:3000

# Backend

$ cd ivi-backend/ <br />
$ python -m venv venv/ # create virtual env <br />
$ source venv/bin/activate # activate virtual env <br />
(venv) $ pip install -r requirements.txt <br />
(venv) $ python main.py <br />

This should start the flask backend dev server on localhost:5000

# ElasticSearch

It is used for storing the data of the files and searching the query.


