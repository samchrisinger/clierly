#!/bin/sh

pkill gunicorn
gunicorn -b 0.0.0.0 --debug application:app