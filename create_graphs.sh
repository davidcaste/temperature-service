#!/bin/bash

cd /home/pi/temperature

gnuplot < indoor.gp > indoor.png
gnuplot < outdoor.gp > outdoor.png

