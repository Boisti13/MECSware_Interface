# Interface for MACSware BS-114 system

![image](https://github.com/Boisti13/MECSware_Interface/assets/76182879/28b5fc84-59cf-4e16-8194-7040abba20cd)


## How to setup:

### Install all neccessary packages
#### Make the script executable
```
chmod +x setup.sh
```
#### Execute the scrip
```
./setup.sh
```
#### Setup static IP for interface eth0
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
