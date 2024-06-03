#!/bin/bash

# Define the path to the config file
CONFIG_FILE="config.env"

# Check if the config file exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: $CONFIG_FILE file not found!"
    return 1
fi


port=$(grep -E '^PORT=' "$CONFIG_FILE" | cut -d '=' -f 2 | tr -d '[:space:]')
# Check if the value is empty
if [ -z "$port" ]; then
    echo "Error: TAG or PORT doesn't meet the requirement $CONFIG_FILE!"
    return 1
fi

# Kill the running server.
sudo kill -9 $(lsof -t -i:"$port") 2>/dev/null


# Check if a virtual environment directory exists
if [ -d "venv" ]; then
  echo "Virtual environment already created, Trying to activate it!"
  # Activate the virtual environment
  source venv/bin/activate
  # Start Gunicorn and append logs to app.log
  python3 -m server
else
  echo "No environment was found!, Trying to create it!"
  echo "run server_setup.sh then try again!"
  return 1
fi
