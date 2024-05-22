#!/bin/bash

#!/bin/bash

# Update and upgrade the package list
echo "Updating and upgrading the package list..."
sudo apt-get update -y
sudo apt-get upgrade -y

# Install Python3, pip, and venv if not already installed
echo "Installing Python3, pip, and venv..."
sudo apt-get install python3 -y
sudo apt-get install python3-pip -y
sudo apt-get install python3-venv -y

# Create a virtual environment
echo "Creating a virtual environment..."
python3 -m venv mecsware_env

# Activate the virtual environment
source mecsware_env/bin/activate

# Install required Python libraries inside the virtual environment
echo "Installing required Python libraries..."
pip install ttkthemes pillow

echo "All necessary libraries and dependencies have been installed in the virtual environment."

# Display a message to indicate completion
echo "Setup is complete. To activate the virtual environment, run 'source mecsware_env/bin/activate'."
echo "You can now run your Python script within the virtual environment."



#   make the script executable
# 1. chmod +x setup.sh
#   Execute the scrip
# 2. ./setup.sh

