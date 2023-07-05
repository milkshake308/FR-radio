#!/bin/bash

SERVICE_NAME="radio-red"
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME.service"
SCRIPT_PATH="/path/to/main.py"
SERVICE_USER=radio
SERVICE_GROUP=radio

if [ "$1" == "install" ]; then
    # Create the service file
    echo "[Unit]
Description=Radio Red Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 $SCRIPT_PATH
ExecStop=/bin/kill -s SIGKILL $MAINPID
WorkingDirectory=$(dirname $SCRIPT_PATH)
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=$SERVICE_NAME
User=$USER
Group=$GROUP
Restart=always

[Install]
WantedBy=multi-user.target" > $SERVICE_FILE

    # Reload systemd daemon
    sudo systemctl daemon-reload

    # Enable and start the service
    sudo systemctl enable $SERVICE_NAME
    sudo systemctl start $SERVICE_NAME

    echo "Service installed and started."
elif [ "$1" == "remove" ]; then
    # Stop and disable the service
    sudo systemctl stop $SERVICE_NAME
    sudo systemctl disable $SERVICE_NAME

    # Remove the service file
    sudo rm $SERVICE_FILE

    # Reload systemd daemon
    sudo systemctl daemon-reload

    echo "Service removed."
else
    echo "Usage: $0 [install|remove]"
    exit 1
fi