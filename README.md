# Event tracking Platform

## Installation

Install pip first
```bash
sudo apt-get install python3-pip
```
Then install virtualenv using pip3
```bash
pip3 install virtualenv 
```
Create virtualenv (Python3.6)
```bash
virtualenv -p python3.6 venv_name
```
Activate virtualenv using
```bash
source venv_name/bin/activate
```
Clone this repo to your machine using
```bash
git clone https://github.com/b4isty/event-tracking-api.git
```
Install requirements.txt file
```bash
pip install -r requirements.txt
```
Go to the project directory 
where manage.py file is located.

To run the migrations files  use this command
```bash
python manage.py migrate
```

To run this project use this command
```bash
python manage.py runserver
```

To run tests use this command
```bash
python manage.py test
```