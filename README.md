https://stackoverflow.com/questions/70955307/how-to-install-google-chrome-in-a-docker-container

https://www.digitalocean.com/community/questions/how-to-keep-running-python-script-all-the-time

https://www.digitalocean.com/community/questions/how-do-i-set-up-chromedriver-path-in-droplets



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

If you are only using a Unix terminal, then you can run the following commands:

wget https://storage.googleapis.com/chrome-for-testing-public/126.0.6478.126/linux64/chrome-linux64.zip
apt-get install unzip
unzip chrome-linux64.zip


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

`chmod +x ~/EchoFinds/main.py`

6. Set up Cron Job

crontab -e

add the following to the crontab file:

`* * * * * /root/EchoFindsVirtualEnv/bin/python /root/echo-finds/main.py > /var/log/echo-finds-cron.log 2>&1`

7. Verify the cron job: crontab -l

8. 