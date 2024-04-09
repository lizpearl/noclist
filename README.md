# Noclist

## Description
This is code for the following assignment https://homework.adhoc.team/noclist/


## Installation
Install python3 and pip.  This code was written and tested with Python 3.12.2 on MacOS 14.4.1 using the Z shell

Create and activate a virtual environment for installation. This example uses `~/.virtualenvs/noclist-venv`
for the path for the new virtual environment.
```
python3 -m venv ~/.virtualenvs/noclist-venv
source ~/.virtualenvs/noclist-venv/bin/activate
```
Clone the repo and install dependencies
```
git clone https://github.com/lizpearl/noclist.git
cd noclist
pip install -r requirements.txt
```

## Usage

### Run the Test Server
Make sure docker is installed, open a new terminal and then run
```
docker run --rm -p 8888:8888 adhocteam/noclist
```

### Run the main script/client
Run this command where you have the virtual environment activated
```
python noclist.py
```
To specify a specific host use
```
python noclist.py --host http://0.0.0.0:8888
```
After running the script you can use the `deactivate` command to exit the 
virtual environment

## Running Tests
In project directory, run 
```
pytest
```

## Troubleshooting
You may get a `notOpenSSLWarning` under certain conditions. More here: https://github.com/urllib3/urllib3/issues/3020