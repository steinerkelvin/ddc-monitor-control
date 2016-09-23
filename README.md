
# dcc-monitor-control

Python script to control monitors using the [`ddcci-tool`](http://jaffar.cs.msu.su/oleg/ddcci/)


## Usage

    monitor_control.py [-h] [-b [x]] [-c [x]] [-d] [-do] [-ds] [-i DEVICE]
    
    arguments:
      -h, --help                show this help message and exit
    
      -b [x], --brightness [x]  Get or set brightness
      -c [x], --contrast [x]    Get or set contrast
    
      -d, --dpms                Set the monitor to sleep
      -do, --dpms-on            Set the monitor to sleep
      -ds, --dpms-stby          Set the monitor to sleep
