#!/bin/bash

python3 -m venv impfung-env
source impfung-env/bin/activate
pip install selenium telegram-send

#### this needs to be adapted to match your distribution package manager
sudo pacman -S geckodriver
##for Macos use - 
# HINt: First run will fail due to GateKeeper. Use CTRL + Rightclick on chromedriver and open it. Then allow execution. 
#brew install geckodriver chromedriver

#########

telegram-send --configure

