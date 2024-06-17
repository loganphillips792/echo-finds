https://stackoverflow.com/questions/70955307/how-to-install-google-chrome-in-a-docker-container

# TODO

- backup sqlite file to S3
- have script automatically deploy to digital ocean

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