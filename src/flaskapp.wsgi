#!/usr/bin/python

from flask import Flask, send_from_directory

from FlaskApp import app as application

application.run(host="0.0.0.0", port=80, debug=True)