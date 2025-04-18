#!/bin/bash

if [ "$1" = "$FOCUSED_WORKSPACE" ]; then
  sketchbar --set $NAME background.drawing=on
else
  sketchybar --set $NAME background.drawing=off
fi
