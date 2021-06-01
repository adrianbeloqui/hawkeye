# hawkeye

## Requirements

- Python 3.6.5

$ export FLASK_APP=app.py
$ python -m flask run --host=0.0.0.0
 * Running on http://0.0.0.0:5000/

## Process of getting devices MAC Addresses

Logged into Raspberry Pi

sudo apt-get install arp-scan
sudo apt-get install nmap

ran:

sudo nmap 192.168.1.0/24 

Took a lot of time and killed the process

Then ran:

sudo arp

From here I got the names and MAC addresses associated to each device connected to the WIFI of the Rasp Pi

Took note of these and then validated that the same MAC addresses appear when running:

sudo arp-scan --retry=8 --ignoredups -I wlan0 --localnet

I will use this command in the Python app because is a lot faster.
