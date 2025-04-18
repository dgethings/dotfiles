#!/usr/bin/env bash

update() {
  # specify the package managers you want the program to use
  # valid manager names "brew" "npm" "yarn" "apm" "mas" "pip" and "gem"
  USE='brew mas'

  # On click update packages
  function click() {
    osascript -e 'display notification "Starting Brew package updates..." with title "Package Updates"'
    bubug && osascript -e 'display notification "Brew packages updated" with title "Package Updates"'
    check
  }
  case "$SENDER" in
  "mouse.clicked")
    click
    ;;
  *)
    check
    ;;
  esac

  # Checks to see if the brew command is avaliable and the package manager is in the enabled list above.
  if [[ -x "$(command -v brew)" ]] && [[ $USE == *"brew"* ]]; then
    # runs the outdated command and stores the output as a list variable.
    brewLIST=$(brew outdated)

    # checks to see if the returned list is empty. If so, it sets the outdated packages list to zero, if not, sets it to the line count of the list.
    if [[ $brewLIST == "" ]]; then
      BREW='0'
      brewLIST=""
    else
      BREW=$(echo "$brewLIST" | wc -l)
    fi

  fi

  # Checks to see if the mas command is avaliable and the package manager is in the enabled list above.
  if [[ -x "$(command -v mas)" ]] && [[ $USE == *"mas"* ]]; then

    # runs the outdated command and stores the output as a list variable.
    masLIST=$(mas outdated)

    # checks to see if the returned list is empty. If so, it sets the outdated packages list to zero, if not, sets it to the line count of the list.
    if [[ $masLIST == "" ]]; then
      MAS='0'
      masLIST=""
    else
      MAS=$(echo "$masLIST" | wc -l)
    fi

  fi

  DEFAULT="0"

  # sum of all outdated packages
  SUM=$((${BREW:-DEFAULT} + ${CASK:-DEFAULT} + ${MAS:-DEFAULT}))

  # icon to be displayed next to number of outdated packages. Feel free to customize. Default: 
  ICON=""

  # icon to be displayed if no packages are outdated. Change to `ZERO=""` if you want the widget to be invisible when no packages are out of date. Default: ✔︎
  ZERO=""

  if [[ $SUM -gt 0 ]]; then
    FINAL="􀐚 ($SUM)"
  else
    FINAL="􀐚"
  fi

  sketchybar -m --set packages label="$FINAL"
}

mouse_entered() {
  sketchybar -m --set packages.total icon.highlight=on \
    label.highlight=on \
    --set packages.details drawing=on \
    --set packages background.drawing=on
}

mouse_exited() {
  sketchybar -m --set packages.total icon.highlight=off \
    label.highlight=off \
    --set packages.details drawing=off \
    --set packages background.drawing=off
}

case "$SENDER" in
"mouse.entered")
  mouse_entered
  ;;
"mouse.exited")
  mouse_exited
  ;;
*)
  update
  ;;
esac
