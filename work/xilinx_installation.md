## NOTE: Here my username is cse, please change paths according to your local machine home directories.
## Download Xilinx_ISE_DS_Lin_14.7_1015_1 (tar) and Xilinx (License) from the given link
```
https://kendra.cse.iitk.ac.in/kendra/CS220L.php
```
## Install dependencies
```
apt install libncurses5 make gitk git-gui libusb-dev build-essential libc6-dev-i386 fxload
```
## Install Xilinx on Ubuntu 22.04
Untar the tar first
```
tar -xvf Xilinx_ISE_DS_Lin_14.7_1015_1.tar
cd Xilinx_ISE_DS_Lin_14.7_1015_1/
./xsetup (Run in Graphical mode), Select WebPack Version and uncheck Cable driver option during installation.
```
## Download usb cable driver
```
cd /opt/Xilinx/
git clone git://git.zerfleddert.de/usb-driver
cd usb-driver/
make
./setup_pcusb /opt/Xilinx/14.7/ISE_DS/ISE
udevadm control --reload-rules
```
## Copy license file
```
cp /home/cse/Xilinx.lic /opt/Xilinx/14.7/ISE_DS/ISE/coregen/core_licenses
```
## Add following lines in .bashrc or every user has need to enter this in their .bashrc
vim /home/cse/.bashrc
```
export PATH=$PATH:/opt/Xilinx/14.7/ISE_DS/ISE/bin/lin64/
export LD_PRELOAD=/opt/Xilinx/usb-driver/libusb-driver.so
```

## How to open ISE
Now just open the terminal and write ise in terminal
