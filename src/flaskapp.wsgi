#!/usr/bin/python

from flask import Flask, send_from_directory
import os

from FlaskApp import app as application

application.run(host="0.0.0.0", port=5000)