# AWS EC2 server toggler
Toggles an AWS EC2 server on or off.

## Environment setup

This repository uses the Boto3 library for interfacing with the AWS API.

### Create the virtual environment

Assuming `python` points to a Python 3.7+ installation. 

```commandline
python -m venv venv
```

Create a virtual environment on the `venv/` directory.

### Activate the virtual environment

The virtual environment activation process varies from one OS to another.
If you created the virtual environment on a Windows machine, go [here](#windows).
Otherwise, go [here](#linux).

#### Linux and WSL

Source the `activate` file on the `bin/` directory inside the newly created virtual environment.

```commandline
source venv/bin/activate
```

#### Windows

Run the `activate` script on the `Scripts/` directory inside the newly-created virtual environment.

```commandline
./venv/Scripts/activate
```

### Install the required packages

Install the required Boto3 package and its dependencies.

```commandline
pip install -r requirements.txt
```

## Usage

When you first run the program, you will be greeted by a 'Waiting configuration' message.
To configure the program, open the `Configuration` menu on the toolbar and input your AWS EC2 credentials and the instance ID.

The script also requires you to input the default region for the specific AWS EC2 instance that you want to monitor/toggle on or off.

### Running

Running the script is very simple and straightforward, as is customary for Python programs.

```commandline
python main.py
```
