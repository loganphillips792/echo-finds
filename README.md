https://stackoverflow.com/questions/70955307/how-to-install-google-chrome-in-a-docker-container

https://www.digitalocean.com/community/questions/how-to-keep-running-python-script-all-the-time

# TODO

- backup sqlite file to S3
- have script automatically deploy to digital ocean
- have it run through Docker

# Echo Finds

Echo is a nymph known for her voice, symbolizing repeated alerts

This app tracks the release of specific products, notifying you when a new product is announced and when it is released. Once a product is released, you will receive a separate email with details on how to obtain it.

# Running locally

## Installing Python depdencies

1. ```python3 -m venv ~/Desktop/EchoFinds```
2. ```source ~/Desktop/EchoFinds/bin/activate``` - this line activates the virtual environment so your Python will use an packages that are installed in it
3. ```which pip``` to verify what is being used (Should point to the one from the virtual environment)
4. ```~/Desktop/EchoFinds/bin/python3 -m pip install --upgrade pip```
5. ```pip install -r requirements.txt```

## Chrome Driver

The Selenium library in Python requires a driver depending on the web browser you are using. In this case, we are using Chrome, so go to this site: https://googlechromelabs.github.io/chrome-for-testing/ and then when the download completes, drag and drop the executable into the root of this folder. The version of chromedriver you need to download will depend on the version of the Chrome browser you are using.

## Running application

1. Go to project root
2. Create environment file (.env)
3. Enable virtual environment
4. python3 main.py

# Running via Docker Compose:

docker-compose up --build


# Support

These are the sites that are currently supported:

- [Owala Color Drop](https://owalalife.com/pages/color-drop)

# Setting  up on Digital Ocean

1. Create a new Droplet

`ssh username@ip_of_droplet`

and then enter your password.

You can find this info via Droplets > Select Droplet > Access

2. Clone Repo

`cd ~`

`git clone https://github.com/loganphillips792/echo-finds.git`

`cd echo-finds`

3. Install Chrome Driver 

4. Set up project and virtual environment

`cd ~/echo-finds`

`vim .env`

```
OWALA_URL=https://owalalife.com/pages/color-drop
CHROME_BROWSER_PATH=/Applications/Google Chrome.app/Contents/MacOS/Google Chrome
TRACK_OWALA=True
DATABASE_NAME=water_bottles.db
```

5. Set up the Virtual Environment

`python3 -m venv ~/EchoFindsVirtualEnv`

`source ~/EchoFindsVirtualEnv/bin/activate`

`pip install -r requirements.txt`


5. Ensure the script is executable

Add a shebang line at the top and then change its permissions


`#!/usr/bin/env python3`

`chmod +x ~/EchoFinds/main.py`

6. Create a Systemd Service file

`sudo vim /etc/systemd/system/echo-finds.service`

```
[Unit]
Description=My Python Script Service
After=multi-user.target

[Service]
Type=simple
ExecStart=/root/EchoFindsVirtualEnv/bin/python /root/echo-finds/main.py
Restart=on-abort

[Install]
WantedBy=multi-user.target
```

7. Reload Systemd and Start your Service


`sudo systemctl daemon-reload`
`sudo systemctl start echo-finds.service`
`sudo systemctl status echo-finds.service`

8. Enable Your Service to Start on Boot

`sudo systemctl enable echo-finds.service`


Additional commands:

Stop the service: `sudo systemctl stop echo-finds.service`
Restart the service: `sudo systemctl restart echo-finds.service`
View logs: Use journalctl. For example: `journalctl -u echo-finds.service`


Remember that when you modify the service file or the script itself, you should usually reload or restart the service to apply the changes.

