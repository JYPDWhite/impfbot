#!/bin/bash

python3 -m venv impfung-env
source impfung-env/bin/activate
pip install selenium telegram-send

#### this needs to be adapted to match your distribution package manager
sudo pacman -S geckodriver
#########

telegram-send --configure

