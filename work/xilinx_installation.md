## Install Xilinx on Ubuntu 22.04
```
tar -xvf Xilinx_ISE_DS_Lin_14.7_1015_1.tar
```
```
apt install libncurses5 make gitk git-gui libusb-dev build-essential libc6-dev-i386 fxload
```
cd /opt/Xilinx
make
./setup_pcusb /opt/Xilinx/14.7/ISE_DS/ISE
udevadm control --reload-rules

## Copy license file

```
cp /home/cse/Downloads/Xilinx.lic /opt/Xilinx/14.7/ISE_DS/ISE/coregen/core_licenses

```


## Add following lines in .bashrc
vim /home/cse/.bashrc
```
export PATH=$PATH:/opt/Xilinx/14.7/ISE_DS/ISE/bin/lin64/
export LD_PRELOAD=/opt/Xilinx/usb-driver/libusb-driver.so
impact
```
