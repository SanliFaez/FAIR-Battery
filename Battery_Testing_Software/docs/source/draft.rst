labphew documentation draft
===========================
Here, I try to collect all the notes about understanding the logic of the code and chosen terms

-------------------------
labphew strategic choices
-------------------------

1. labphew is mainly a functioning template for educating beginners
2. users are encouraged to edit the code but preserve the folder structure
3. labphew is limited controlling only two devices, one camera and one data acquisition card
4. controllers of the sister packages should be rather easy to import
5. labphew is not a support package for other code and backward compatibility is unnecessary
6. new applications are created through writing a new model
7. working with labphew should be fun


-------------------------------
submodules and name conventions
-------------------------------

* submodules
    * core
    * controller
    * model
    * view

* currently chosen core structure
    - view
        * start : to make a unique entry point for starting the program with settings
        * scan_view : GUI for viewing progress of non-recursive routines
        * monitor_view : GUI for continuous monitoring of the experiment and calling single routines
        * blink_view : the simplest interactive example for absolute beginners
        * config_view : to adjust the essential measurement parameters as alternative to editing and recalling the config-file
    - model
        * contains one model file per device (dummy or real) plus one model file for the desired application
        * blink_controller : didactic example
    - controller
        * one folder per device including drivers and controllers
        * _blank_controller : template for writing a new driver
        * blink_controller : didactic example
    - core
        standards and defaults necessary to preserve consistency as much as possible


* labphew name conventions
    * Operator: Class containing group operations necessary for a measurement ("Experiment" in PFTL)
    * operation: each function in the Operator class
    * MonitorWindow: Class containing the GUI and interactions for monitoring operations that run continuously
    * ScanWindow: Class containing the GUI and update inquiries for one-time operations that can be called from another window or command line
    * WorkThread: same as WorkThread in PFTL

* other types of folders or files:
    * adapt : folder containing python routines from other packages that are in progress of importing
    * attic : folder containing old versions that can be deleted before each release
    * blink : files in the program hierarchy that can be used to guide beginners
    * _blank : skeleton of files that can be used to develop a new driver or model