#!/bin/bash

cd "$(dirname "$0")"

function cp_if_ne {
    if [ ! -f "$2" ]
        then
        echo "Backing up file $1"
        return `cp "$1" "$2"`
    fi

    return "0"
}

function check_error {
  CP_RESULT="$?"
  # Backup
  if [ "$CP_RESULT" -ge "1" ]
    then
    echo -e "\033[31mError during installation, are you sure you have a valid Ableton Live installation?" > /dev/tty
    exit 1
  fi
}


function find_ableton_path {

  ABLETON_PATHS=()
  while IFS=  read -r -d $'\0'; do
      ABLETON_PATHS+=("$REPLY")
  done < <(find '/Applications' -name 'Ableton*.app' -maxdepth 1 -print0)



  NUM_INSTALLS="${#ABLETON_PATHS[@]}"
  if [ "$NUM_INSTALLS" -gt "1" ]
    then
    PS3='Where do you want to install Ubermap? '

    echo -e "\033[33m(!) More than one Ableton Live installation found."  > /dev/tty
    select opt in "${ABLETON_PATHS[@]}"
    do
        if [ "$REPLY" -le "$NUM_INSTALLS" ]
        then
          NUM=$(($REPLY - 1))
          SELECTED_ABLETON="${ABLETON_PATHS[$NUM]}"
          break
        else
          echo "Invalid choice" > /dev/tty
        fi
    done
  elif [ "$NUM_INSTALLS" -gt "0" ]
    then
    echo -e "\033[33mOne Ableton Live installation found at path: ${ABLETON_PATHS[0]}" > /dev/tty
    SELECTED_ABLETON="${ABLETON_PATHS[0]}"
  else
    echo -e "\033[31mNo Ableton Live installation found." > /dev/tty
    SELECTED_ABLETON=""
  fi

}

SELECTED_ABLETON=""
find_ableton_path
LIVE_MIDI_REMOTE_PATH="${SELECTED_ABLETON}/Contents/App-Resources/MIDI Remote Scripts"
echo "$(tput sgr0) --> Installing into ${LIVE_MIDI_REMOTE_PATH} ... "

cd ${0%/*}

cp_if_ne "$LIVE_MIDI_REMOTE_PATH/Push/__init__.pyc" "$LIVE_MIDI_REMOTE_PATH/Push/__init__.py.ubermap-backup"
check_error
cp_if_ne "$LIVE_MIDI_REMOTE_PATH/Push2/__init__.pyc" "$LIVE_MIDI_REMOTE_PATH/Push2/__init__.pyc.ubermap-backup"
check_error

# Copy
mkdir -p "$LIVE_MIDI_REMOTE_PATH/Ubermap"
cp ../Common/__init__.py "$LIVE_MIDI_REMOTE_PATH/Ubermap/"
check_error

cp ../Common/configobj.py "$LIVE_MIDI_REMOTE_PATH/Ubermap/"
cp ../Common/UbermapLibs.py "$LIVE_MIDI_REMOTE_PATH/Ubermap/"
cp UbermapDevices.py "$LIVE_MIDI_REMOTE_PATH/Ubermap/"
cp UbermapDevicesPatches.py "$LIVE_MIDI_REMOTE_PATH/Ubermap/"
cp UbermapVisualisation.py "$LIVE_MIDI_REMOTE_PATH/Ubermap/"

cp Push/__init__.py "$LIVE_MIDI_REMOTE_PATH/Push/"
cp Push2/__init__.py "$LIVE_MIDI_REMOTE_PATH/Push2/"

# Copy config
mkdir -p ~/Ubermap/Devices
cp_if_ne ../Config/devices.cfg ~/Ubermap/
cp_if_ne ../Config/global.cfg ~/Ubermap/

# Remove .pyc
rm "$LIVE_MIDI_REMOTE_PATH/Ubermap/*.pyc" 2> /dev/null
rm "$LIVE_MIDI_REMOTE_PATH/Push/__init__.pyc" 2> /dev/null
rm "$LIVE_MIDI_REMOTE_PATH/Push2/__init__.pyc" 2> /dev/null

echo -e "\033[32mUbermap installed - now restart Ableton Live. "
