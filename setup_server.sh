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

# Update and upgrade system packages
sudo apt-get update && sudo apt-get upgrade -y

# Install python3-venv if not already installed
sudo apt install python3-venv -y


# Kill any running process on port 5000
echo "=====> Killing process running on port '$port'"
sudo kill -9 $(lsof -t -i:$port) 2>/dev/null
if [ $? -eq 0 ]; then
    echo "=====> Process on port $port killed."
else
    echo "=====> No process was running on port $port."
fi


# Function to check if the virtual environment is activated
is_venv_activated() {
    [[ -n "$VIRTUAL_ENV" ]]
}

# Get the directory of the current script
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)


# Check if a virtual environment directory exists
if [ -d "$SCRIPT_DIR/venv" ]; then
    echo "=====> Virtual environment already exists. Activating it..."
    source "$SCRIPT_DIR/venv/bin/activate"
else
    echo "=====> No virtual environment found! Creating one..."
    python3 -m venv "$SCRIPT_DIR/venv"
    if [ $? -eq 0 ]; then
        echo "=====> Virtual environment successfully created. Activating it..."
        source "$SCRIPT_DIR/venv/bin/activate"
    else
        echo "=====> Failed to create virtual environment."
        return 1
    fi
fi

# Verify that the virtual environment is activated
if is_venv_activated; then
    echo "=====> Virtual environment is activated."

    # Check if requirements.txt exists and install packages
    if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
        echo "=====> Installing packages from requirements.txt..."
        pip install -r "$SCRIPT_DIR/requirements.txt"
        if [ $? -eq 0 ]; then
            echo "=====> Requirment packages installed successfully!"
            echo "=====> Initial migrations started, It may take while!"
        else
            echo "Failed to install packages from requirements.txt, Existing....!"
            return 1
        fi
    else
        echo "requirements.txt not found. Existing....!"
        return 1
    fi
else
    echo "Failed to activate the virtual environment, Existing....!"
fi

chmod +x run.sh

# Create Flask service file
FLASK_SERVICE_FILE="/etc/systemd/system/RTC-backend.service"
if [ -f "$FLASK_SERVICE_FILE" ]; then
    echo "=====> Service file already exists. Stopping the service..."
    sudo systemctl stop RTC-backend.service
fi

echo "=====> Creating/Updating Flask service file at $FLASK_SERVICE_FILE..."

sudo bash -c "cat > $FLASK_SERVICE_FILE" <<EOL
[Unit]
Description=RealitY Connect Backend Service
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=$SCRIPT_DIR
ExecStart=$SCRIPT_DIR/run.sh
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOL

# Reload systemd manager configuration
sudo systemctl daemon-reload

#Enable and start the new service
sudo systemctl enable RTC-backend.service
sudo systemctl start RTC-backend.service

echo "=====> Flask service RTC-backend.service has been created/updated and started."
echo "=====> run 'sudo service RTC-backend.service status' to see the service status"
