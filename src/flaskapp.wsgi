#!/usr/bin/python

from flask import Flask, send_from_directory

from FlaskApp import app as application

application.run(host="127.0.0.1", port=5000, debug=True)