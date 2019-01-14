#! /usr/bin/env bash

export FLASK_APP=cars_api
export FLASK_ENV=development

pip install -e .
flask run
