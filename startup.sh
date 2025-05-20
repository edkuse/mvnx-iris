#!/bin/bash

# Install dependencies
pip install -r requirements.txt
pip install Werkzeug==2.2.2

# Start the application
gunicorn --bind=0.0.0.0 --timeout 600 run:app
