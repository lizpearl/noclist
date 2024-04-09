# Noclist

## Description
This is code for the following assignment https://homework.adhoc.team/noclist/


## Installation
Install python3.  This code was written and tested with Python 3.12.2 on MacOS 14.4.1.  

Create a virtual environment for installation. The example uses the ~/.virtualenv directory for virual environments.
```
python3 -m venv ~/.virtualenvs/venv-noclist
source ~/.virutalenvs/venv-noclist/bin/activate
```

```
git clone https://github.com/lizpearl/noclist.git
cd noclist
pip install -r requirements.txt
```


## Usage

### Run the Test Server
Make sure docker is installed and then run
```
docker run --rm -p 8888:8888 adhocteam/noclist
```

### Run the main script
```
python noclist.py
```
To specify a specific host use
```
python noclist.py --host http://0.0.0.0:8888
```


## Running Tests
In project directory, run 
```
pytest
```