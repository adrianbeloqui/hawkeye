from flask import Flask
from flask import render_template
import subprocess
import requests

import settings

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/motion/connected-devices')
def connected_devices():
    connected_devices, valid_devices = _devices_connected()
    devices_names = []
    for device in valid_devices:
        devices_names.append(settings.DEVICE_NAME_MAP.get(device))
    return render_template('connected_devices.html', connected_devices=connected_devices, devices=devices_names)

@app.route('/motion/auto-activate')
def automatically_activate_motion_detection():
    activated = False
    _, valid_devices = _devices_connected()
    if len(valid_devices) == 0:
        activation = requests.get('{0}/1/detection/start'.format(settings.HAWKEYE_URL))
        if activation.status_code == 200:
            activated = True
    else:
        activation = requests.get('{0}/1/detection/pause'.format(settings.HAWKEYE_URL))
        if activation.status_code == 200:
            activated = False
    return render_template('automatically_activate.html', activated=activated)

@app.route('/motion/manually-activate')
def manually_activate_motion_detection():
    activated = False
    activation = requests.get('{0}/1/detection/start'.format(settings.HAWKEYE_URL))
    if activation.status_code == 200:
        activated = True
    return render_template('manually_activate.html', activated=activated)

@app.route('/motion/manually-deactivate')
def manually_deactivate_motion_detection():
    deactivated = False
    deactivate = requests.get('{0}/1/detection/pause'.format(settings.HAWKEYE_URL))
    if deactivate.status_code == 200:
        deactivated = True
    return render_template('manually_deactivate.html', deactivated=deactivated)

@app.route('/1/detection/pause')
def mock():
    return 'Yes', 200

@app.route('/1/detection/start')
def mock2():
    return 'Yes', 200

def _find_devices_connected():
    # getting meta data of the wifi network
    meta_data = None
    try:
        # Local Testing
        meta_data = subprocess.check_output(['sudo', 'arp-scan', '--retry=1', '--ignoredups', '-I', 'enp0s3', '--localnet'])
        # Prod
        #meta_data = subprocess.check_output(['arp-scan', '--retry=4', '--ignoredups', '-I wlan0', '--localnet'])
    except Exception as e:
        print('An exception happened trying to get the devices: ' + str(e))
        return []
    # decoding meta data from byte to string
    data = meta_data.decode('utf-8', errors ="backslashreplace")
    # splitting data by line by line
    # string to list
    data = data.split('\n')
    # creating a list of wifi devices mac addresses
    devices = []
    # traverse the list
    for i in data:
        device_line = i.split('\t')
        if len(device_line) == 3:
            devices.append(device_line[1])
    return devices

def _devices_connected():
    connected_devices = _find_devices_connected()
    devices = []
    for device in connected_devices:
        if device in settings.VALID_DEVICES:
            devices.append(device)
    return (connected_devices, devices)