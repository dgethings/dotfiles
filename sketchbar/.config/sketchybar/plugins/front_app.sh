#!/bin/bash

# Some events send additional information specific to the event in the $INFO
# variable. E.g. the front_app_switched event sends the name of the newly
# focused application in the $INFO variable:
# https://felixkratz.github.io/SketchyBar/config/events#events-and-scripting

case $INFO in
"Warp")
  ICON="􀩼"
  ;;
"Arc")
  ICON="􀎬"
  ;;
"Code")
  ICON=󰨞
  ;;
"Calendar")
  ICON="􀉉"
  ;;
"Discord")
  ICON=
  ;;
"FaceTime")
  ICON=
  ;;
"Finder")
  ICON="􀈕"
  ;;
"kitty")
  ICON=󰄛
  ;;
"Messages")
  ICON="􀌤"
  ;;
"Notion")
  ICON=󰎚
  ;;
"Preview")
  ICON=
  ;;
"Mail")
  ICON="􀈣"
  ;;
*)
  ICON="􀑋 $INFO"
  ;;
esac

sketchybar --set "$NAME" icon="$ICON"
sketchybar --set "$NAME.name" label="$INFO"
