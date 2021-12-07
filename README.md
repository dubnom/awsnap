# awsnap
Fix Aw Snap Chromium errors and popups


## What is "Aw Snap!"?
Aw Snap! is a recurring error message in Chromium on a Raspberry Pi.
It is likely that this error message has popped up on other platforms as well.
Chromium (as of writing this) doesn't have a way of auto-reloading the offending
web page, which renders kiosks and other dedicated displays useless after the error.

This simple Python3 script polls the Chromium state file looking for changes
in the "render crash count" (which are associated with the "Aw Snap!" messages).
A shell script is then executed to refresh the web page (or do whatever else you
may need to do).

included in this package is a shell script called 'refresh-chromium.sh' which uses
'xdotool' to send messages to the Chromium browser through Xwindows.

##Installation:

Install 'xdotool':
```
sudo apt install xdotool
```

Copy 'awsnap.py' and 'refresh-chromium.sh' into the home directory of the user
running Chromium.  The default is '/home/pi', this can be changed by modifying 'awsnap.py'
or instantiating your own 'awSnap' object.

Edit '/etc/rc.local' and add '/home/pi/awsnap.py >/var/log/awsnap.log 2>&1 &' near the end of
the file, before 'exit 0'.  You will have to be a supervisor to do this.

Reboot your machine, and "Aw Snap!" will largely be an annoyance of the past.  You'll
still occasionally get a few second delay before and during an event, but this can
be somewhat controlled by the polling interval (in 'awsnap.py', which defaults to 10 seconds).

Hopefully, the Chromium folks will either fix whatever causes the error message, or
add a 'awsnap_restart' command-line flag.

Enjoy.
