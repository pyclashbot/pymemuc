# memuc.exe documentation

## Create a new VM

    Usage:     memuc create
    memuc create 44    //create a certain version of Android
    memuc create 51
    memuc create 71
    memuc create 76  (Android 7.1 64-bit)
    Sample:   memuc create //Create a new VM

## Delete a existed VM

    Usage:     memuc remove <-i vmindex | -n vmname>
    Sample:   memuc remove -i 0 //Delete the MEmu VM

## Clone a existed VM

    Usage:     memuc clone <-i vmindex | -n vmname> [-r nametag] [-t]
    [-t] Return without waiting for the end of the task, and get the task id number
    Sample:   memuc clone -i 1 //Clone the MEmu_1 VM

## Export/Backup a VM to a file

    Usage:     memuc export <-i vmindex | -n vmname> <ovafile> [-t]
    <ovafile> Export to ova file type
    [-t] Return without waiting for the end of the task, and get the task id number
    Sample:   memuc export -n MEmu_1 c:\1.ova //Export MEmu_1 VM to 1.ova file in C drive

## Import/Restore a VM from a existed ova file

    Usage:     memuc import <ovafile> [-t]
    <ovafile> ova file type
    <memufile> memu file type (supported by 7.1.3 version and later)
    [-t] Return without waiting for the end of the task, and get the task id number
    Sample:   memuc import c:\1.ova //Import a VM from 1.ova file in C drive

## Start a existed VM

    Usage:     memuc start <-i vmindex | -n vmname> [-t]
                        [-t] Return without waiting for the end of the task, and get the task id number
    Sample:   memuc start -n MEmu_2 //Start the MEmu_2 VM

## Stop a running VM

    Usage:     memuc stop <-i vmindex | -n vmname> [-t]
                        [-t] Return without waiting for the end of the task, and get the task id number
    Sample:   memuc stop -n MEmu //Stop the MEmu VM

## Stop all running VMs

    Usage:     memuc stopall
    Sample:   memuc stopall //Stop all the running VMs

## List information of all VMs

    Usage:     memuc listvms [–running] [-s]
                        [–running] List information of all running VMs
    Sample:   memuc listvms //List information like index, title, window handle, status, pid.
    Sample:   memuc listvms -s //Display disk information

## whether VM is running or not

    Usage:     memuc isvmrunning <-i vmindex | -n vmname>
    Sample:   memuc isvmrunning -n MEmu_3 //Check whether VM is running or not

## Sort out all VM windows

    Usage:     memuc sortwin
    Sample:   memuc sortwin //Sort out all VM windows

## Reboot VM

    Usage:     memuc reboot <-i vmindex | -n vmname> [-t]
                        [-t] Return without waiting for the end of the task, and get the task id number
    Sample:  memuc reboot -i 0 //Reboot VM

## Rename VM

    Usage:    memuc rename <-i vmindex | -n vmname> <title>
    Sample:  memuc rename -i 0 “MEmu_1” //Rename VM

## Check asynchronous task status, like clone, export, import, start and stop.

    Usage:     taskstatus <taskid>
    Sample:   taskstatus 7baf735f-c877-4836-aaf9-ccca67296a8f //Check the status of task 100, it will return success, running, or failed.

## Get configuration data of VM

    Usage:     memuc getconfigex <-i vmindex | -n vmname> <key>
                    <key> configuration key name
    Sample:   memuc getconfigex -i 0 memory //Get the memory size of MEmu VM

## Set configuration data of VM

    Usage:     memuc setconfigex <-i vmindex | -n vmname> <key> <value>
                    <key> configuration key name
    Sample:   memuc setconfigex -i 0 cpus 4 //Set the number of CPU core as 4

## Install Apk in VM (Android)

    Usage:     memuc installapp <-i vmindex | -n vmname> <apkfile> [-s]
                    <apkfile> apk filepath
    [-s] Create a shortcut on the desktop after installation (7.1.3 version and later)
    Sample:   memuc installapp -n MEmu_1 c:\test.apk //Install test.apk into MEmu_1 VM

## Uninstall App from VM

    Usage:     memuc uninstallapp <-i vmindex | -n vmname> <packagename>
                    <packagename> app package name
    Sample:   memuc uninstallapp -i 1 com.microvirt.test //Uninstall this app from MEmu_1 VM

## Start App in VM

    Usage:     memuc startapp <-i vmindex | -n vmname> <packageactivity>
                    <packageactivity> app main activity
    Sample:   memuc startapp -i 1 com.android.settings/.Settings //Start Android settings in MEmu_1 VM

## Stop App in VM

    Usage:     memuc stopapp <-i vmindex | -n vmname> <packagename>
                    <packagename> app package name
    Sample:   memuc stopapp -i 1 com.android.settings //Stop Android settings in MEmu_1 VM

## Trigger Android keystroke

    Usage:     memuc sendkey <-i vmindex | -n vmname> <key>
                    <key> back | home | menu | volumeup | volumedown
    Sample:   memuc sendkey -i 0 home //Trigger home key in MEmu VM

## Trigger shake

    Usage:     memuc shake <-i vmindex | -n vmname>
    Sample:   memuc shake -i 1 //Trigger shake in MEmu_1 VM

## Connect internet in Android

    Usage:     memuc connect <-i vmindex | -n vmname>
    Sample:   memuc connect -i 2 //Connect internet in MEmu_2 VM

## Disconnect internet in Android

    Usage:     memuc disconnect <-i vmindex | -n vmname>
    Sample:   memuc disconnect -i 2 //Disconnect internet in MEmu_2 VM

## Input text to Android

    Usage:     memuc input <-i vmindex | -n vmname> <text>
    Sample:   memuc input -i 0 “Hello World!” //Input “Hello World!” text into MEmu VM

## Rotate VM window

    Usage:     memuc rotate <-i vmindex | -n vmname>
    Sample:  memuc rotate -i 0 //Rotate the first VM

## Execute command in Android

    Usage:     memuc <-i vmindex | -n vmname> execmd <guestcmd>
    Sample:   memuc -i 1 execcmd “getprop persist.sys.language” //Execute “getprop” command to get Android language in MEmu_1 VM

## Change GPS latitude and longitude

    Usage:     memuc setgps <-i vmindex | -n vmname> <longitude> <latitude>
    Sample:  memuc setgps -i 0  30.978785 121.824455 //Set current longitude 30.978785, latitude 121.824455

## Obtain the public IP address

    Usage:    memuc -i 0 execcmd “wget -O- whatismyip.akamai.com”

## Zoom in (Supported by version 6.2.6 and later)

    Usage:    memuc zoomin <-i vmindex | -n vmname>
    Sample:  memuc zoomin -i 0 //Zoom in the content

## Zoom out (Supported by version 6.2.6 and later)

    Usage:     memuc zoomout <-i vmindex | -n vmname>
    Sample:  memuc zoomout -i 0 //Zoom out the content

## Get a list of third-party apps in the emulator (supported by 7.1.3 and later)

    Usage:     memuc getappinfolist <-i vmindex | -n vmname>
    Sample:  memuc getappinfolist -i 0 //Show the third-party app list of MEmu

## Set the value of acceleration of gravity (supported by 7.1.3 and later)

    Usage:    memuc accelerometer <-i vmindex | -n vmname> <-x xvalue> <-y yvalue> <-z zvalue>
    Sample:  memuc accelerometer  -i 0 <-x 0.0> <-y 8.9> <-z 4.5> //Set the gravity acceleration value to 0, 8.9, 4.5

## Create desktop shortcuts for Android applications (supported by 7.2.5 and later)

    Usage:    memuc createshortcut <-i vmindex | -n vmname> <packagename>
    Sample:  memuc createshortcut -i 0  com.android.settings //Create a desktop shortcut for the Settings app

## List all emulator information

    Usage: memuc listvms [-i vmindex | -n vmname]
    Sample:  memuc listvms //List the simulator index, title, top-level window handle, whether to start the simulator, process PID information, simulator disk usage

## ADB command

    Usage:     memuc <-i vmindex | -n vmname> adb <adbcmd>
    Sample:   memuc -i 0 adb “remount”
