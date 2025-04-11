Time Application
An interactive visualization of various time systems presented as concentric circles.

Project Description
Time Application is a tool for visualizing different time measurement systems in one coherent interface. The individual time systems are presented as concentric circles, which allows for simultaneous comparison and observation of different ways humanity perceives and measures time.

Time Systems
The application includes the following time systems:

Local Time - a classic analog clock displaying the current local time

Hebrew Calendar - a traditional Hebrew calendar with months and days

Atomic Time - precise time retrieved from NTP servers

Pulsar Time - a simulation of pulsars as natural cosmic clocks

Earth’s Rotation - a visualization of the Earth’s rotation with day and night division

Astronomical Year - the Earth’s orbit around the Sun with indications of seasons and zodiac signs

Installation and Execution
System Requirements
Python 3.8 or newer

PyQt5

Additional libraries: numpy, pytz, ntplib

Installation Instructions
Unpack the archive to a chosen directory

Open a terminal/console and navigate to the unpacked directory

Install the required dependencies:


pip install PyQt5 numpy pytz ntplib

Run the application:

python main.py
Using the Application
After launching the application, you will see the main window displaying the time systems as concentric circles. You can:

Pan and zoom the view using the mouse

Click on individual elements to obtain more information

Configure various display options through the menu and toolbar

Change time zones and other settings

Code Structure
The project code is organized as follows:

main.py - the main file that starts the application

ui_mainwindow.py - definition of the main application window

style.qss - stylesheet for the user interface

systemy_czasowe/ - directory with modules of various time systems

widgets/ - directory with custom widgets and components

resources/ - directory with resources (icons, images, etc.)
