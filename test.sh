#!/bin/bash

PYTHONPATH=src python3 -m unittest discover -s test -p "*.py"
