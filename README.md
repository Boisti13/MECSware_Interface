# Interface for MACSware BS-114 system

![image](https://github.com/Boisti13/MECSware_Interface/assets/76182879/28b5fc84-59cf-4e16-8194-7040abba20cd)


## How to setup:
### Make the script executable
```
chmod +x setup.sh
```
### Execute the scrip
```
./setup.sh
```

### If neccessary, disable and enable eth0 (static setup, connected to BS-114)

Disable Interface eth0
```
sudo ifconfig eth0 down
```
Enable Interface eth0
```
sudo ifconfig eth0 up
```
