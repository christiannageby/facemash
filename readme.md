# Facemash
A clone of the facemash website from [The Social Network](https://www.imdb.com/title/tt1285016/) however there is no need to fetch the images from public webservers since there is an image upload function.

## Disclaimer
Regarding the aspect of morale and respect this application may provoke some, this is not the purpose. The solely intention of this application is to implement the ELO-ranking system in an easy and fun manner. 

## Installation
There is a few steps to be done to install the application first off you'll need to copy the configuration sample to config.py and set the correct parameters. Once it is done you may create the database, import db from facemash.py and issue the `db.create_all()` method. 

Configure any uWGSI server to run the application or use the flask built in webserver to serve the webapp.
