# Kitchen Radio

Kitchen Radio that starts playing the last selected channel when powered on. This is accomplished by using systemd services that start on boot. Radio URLs are stored as a simple list inside the text file `radios.txt`.
Channels can be switched with a GPIO connected button.

There are two programs running:
  1. A python script that reacts to GPIO input and toggles the according systemd service, eg.: `radio@2`. The last number indicates the line number in `radios.txt` and is used as a parameter.

  2. The shell script `radio.sh` that is started by the systemd service (see above). It gets the radio index as commandline argument, gets the url from `radios.txt` and starts mplayer with it.


## Requirements
- Raspberry Pi or comparable device
- python3
- linux distro that uses systemd

## Customize

- edit list of radios to play, inside `radios.txt`. At the moment you also have to manually set the amount of radios bia `MAXRADIOS` inside `radio_gpio.py`
- change the GPIO pin to then one your channel switch button actually is connected via `BUTTONPIN` in `radio_gpio.py`


## Install

0. Connect a simple push button to a GPIO pin

1. Modify `WorkingDirectory` and `ExecStart` inside **both** system services inside `./systemd-services` to match yours paths.

2. Copy both systemd services to your preferred systemd service location (for example: `/etc/systemd/system/`)

3. Enable the GPIO listening service with: `systemctl enable radio-gpio.service && systemctl start radio-gpio.service`
  
You only need to enable this one. The other ones is handled and toggled by `radio-gpio` on button presses.

Thats all! Now try out your GPIO connected button and listen to your radio. :)
