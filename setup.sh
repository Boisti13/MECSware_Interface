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

echo "All necessary libraries and dependencies have been installed."

# Display a message to indicate completion
echo "Setup is complete. You can now run your Python script."


#   make the script executable
# 1. chmod +x setup.sh
#   Execute the scrip
# 2. ./setup.sh

