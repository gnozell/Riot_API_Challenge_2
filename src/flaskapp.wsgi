#!/usr/bin/python

from flask import Flask, send_from_directory

from FlaskApp import app as application

# remove this line if you want to run this on an apache server
# then edit __init__.py to run it instead
application.run(host="0.0.0.0", port=80)