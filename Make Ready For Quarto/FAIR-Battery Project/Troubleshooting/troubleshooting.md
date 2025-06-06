# Troubleshooting

Is something not working right? Hopefully the steps below will help you
get your battery up and running again, otherwise please submit an issue.

Open [this](bug_report.md) file for more information on
how to submit an issue and what to include. In Community, there will be more info on how to send this file to the correct contact.

## Hardware Troubleshooting

**Troubleshooting Steps:**

> 1.  Turn it off and on
> 2.  Check the connections
> 3.  Check the voltage test points

## Software Troubleshooting

Simple troubleshooting can be done by reading the popup errors that the
Battery Testing software provides. More sophisticated issue however may
require you to read the errors that appear in the terminal window of
your code editor.

**ImportError: No module named \'Battery_Testing_Software\'**
\^\^\^\^\^\^\^\^\^\^\^\^\^\^\^\^\^\^\^\^\^\^\^\^\^\^\^ This occurs when
your python project path variable has not been set. To fix this open a
terminal and navigate to the project root directory:

``` 
cd FAIR-Battery/
```

Next set the path to the current directory.

Mac / Linux:

``` 
export PYTHONPATH=.
```

Windows:

``` 
set PYTHONPATH=%PYTHONPATH%;.
```

If you want to be sure the path is set correctly, you can run the
following one liner in your terminal to list your paths. As ever, use
either `python` or `python3` depending on which works on your system.

``` 
python -c "import sys; print(sys.path)"
```

### **FileNotFoundError: Could not find module \'dwf\' (or one of its dependencies)**

This happens when the [waveforms
SDK](https://mautic.digilentinc.com/waveforms-download) is not installed
correctly. It is a dependency of the dwf module, and therefore essential
for controlling the AD2. For a great startup guide visit:
<https://digilent.com/reference/software/waveforms/waveforms-3/getting-started-guide>

NOTE: Make sure to not just install waveforms, but most importantly
install the runtime and SDK.

On windows this is just a matter of checking the following options in
the installer.

![Installing waveforms sdk on windows](_static/Windows_waveforms.png)

On mac once the installer is opened, drag not only the waveforms app to
applications, but also the dwf.framework to your Frameworks folder.

![Installing waveforms sdk on mac](_static/Mac_waveforms.png)

### **Error: AD2 Device not connected**

Check the USB connection to the Analog Discovery 2 board. Try various
USB cables in case one has broken or does not have data lines. Perhaps
also try the same USB cable with another device that requires data
lines, to make sure this isn\'t the issue. If all as well, the AD2
should appear as a USB device.
