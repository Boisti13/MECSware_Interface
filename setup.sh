#!/bin/bash

# Update and upgrade the package list
echo "Updating and upgrading the package list..."
sudo apt-get update -y
sudo apt-get upgrade -y

# Install Python3 and pip if not already installed
echo "Installing Python3 and pip..."
sudo apt-get install python3 -y
sudo apt-get install python3-pip -y

# Install Tkinter
echo "Installing Tkinter..."
sudo apt-get install python3-tk -y

# Install required Python libraries
echo "Installing required Python libraries..."
pip3 install ttkthemes pillow --break-system-packages

# Install imageTK
echo "Installing imageTK..."
sudo apt-get install python3-pil python3-pil.imagetk

echo "All necessary libraries and dependencies have been installed."

# Get the directory where the script is located
SCRIPT_DIR="$(dirname "$(realpath "$0")")"

echo "Creating desktop shortcut..."

# Define the source and destination paths
SOURCE_FILE="$SCRIPT_DIR/MECSware_Interface.desktop"
DESTINATION_DIR="/home/pi/Desktop"

# Check if the source file exists
if [ -f "$SOURCE_FILE" ]; then
    # Copy the file to the destination directory
    cp "$SOURCE_FILE" "$DESTINATION_DIR"
    echo "MECSware_Interface.desktop has been copied to $DESTINATION_DIR"
else
    echo "MECSware_Interface.desktop not found in $SCRIPT_DIR"
fi

chmod +x /home/pi/Desktop/MECSware_Interface.desktop

# Display a message to indicate completion
echo "Setup is complete. You can now run your Python script."


#   make the script executable
# 1. chmod +x setup.sh
#   Execute the scrip
# 2. ./setup.sh

