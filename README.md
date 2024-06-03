# Interface for MACSware BS-114 system

![image](https://github.com/Boisti13/MECSware_Interface/assets/76182879/28b5fc84-59cf-4e16-8194-7040abba20cd)

Interface to interact with the MACSware BS-114 5G system

## How to setup:

### Install all necessary packages
#### Install GIT
This step is optional, but needed if the next step thows an error. The shell script will initialise an update and upgrade as well
```
sudo apt-get update -y && sudo apt-get upgrade -y
```
```
sudo apt-get install git-all -y
```
```
git version
```
#### Clone GIT repro
```
cd Desktop
```
```
git clone https://github.com/Boisti13/MECSware_Interface
```
or
```
git clone https://gitlab.rhrk.uni-kl.de/kolbgrun/MECSware_Interface
```
```
cd MECSware_Interface
```
check if repro was cloned
```
ls
```
#### Make the script executable

```
chmod +x setup.sh
```
#### Execute the scrip
```
./setup.sh
```
### Change display system from Wayland to X11
```
sudo raspi-config
```
_-> Advanced Options -> (A6) Wayland -> (W1) X11 -> reboot_

### Run MECSware GUI
```
python3 MECSware_GUI.py
```


### Setup static IP for interface eth0
Check which interface you want to use to connect the BS-114 system
```
ifconfig
```
open the interface config
```
sudo nano /etc/network/interfaces
```
add the following
```
iface eth0 inet static
address 10.0.1.11
netmask 255.255.255.0
gateway 10.0.1.1
```

#### If neccessary, disable and enable eth0 (static setup on eth0, connected to BS-114)

Disable Interface eth0
```
sudo ifconfig eth0 down
```
Enable Interface eth0
```
sudo ifconfig eth0 up
```
