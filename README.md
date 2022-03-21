# Chatbot

![CI](https://github.com/franksh/chatbot/actions/workflows/build.pipeline.yml/badge.svg)
![Coverage badge](tests/coverage-badge.svg)

A language learning Chatbot

## Overview

tbd

## Usage

### Installation

The package uses `python3.9`.

First clone the repo:

```bash
git clone git@github.com:franksh/chatbot.git
cd chatbot
```

It is recommended to also set up and activate a
virtual environment, for example using

```bash
pip install virtualenv
virtualenv venv
source venv/bin/activate
```

Then, install the application and dependencies as a package in development mode using

```bash
make install
```

which is equivalent to running

```bash
pip install -e .
```

which installs the application as a package in developer (local edit) mode.

### Running the application

Before running the application, initialize the user database

```bash
flask init-db
```

Start the application from the root project directory using

```bash
flask run
```

If the application is installed, you can also start
it from anywhere using

```bash
export FLASK_APP=chatbot
flask run
```

### Useful commands

- `flask run`: Run the application.
- `flask init-db`: Initialize the database.
- `flask shell`: Start an interactive Python shell in the application context, with an app instance imported

## Testing

### Running Unit Tests

You can run tests using

```bash
pytest
```

Add the `-v` flag to show the result for each test function.

To measure the code coverage of the tests, use the `coverage` command:

```bash
coverage run -m pytest
```

You can view the coverage report using

```bash
coverage report
# or
coverage html
```

### Testing in the Flask shell

The flask application can also be tested from the shell.

Start the shell with

```bash
flask shell
```

In the shell, you can test endpoints like so:

```python
>>> client = app.test_client()
>>> client.get('/')
<WrapperTestResponse streamed [200 OK]>
>>> client.post(
      '/auth/register',
      data={'username': username, 'password': password}
    )
```

### Load testing with locust

To test the application under user traffic, do

```bash
cd tests/
locust
```

which will open a dashboard at `http://0.0.0.0:8089/`. There you can simulate users retrieving different endpoints. More complex fuctionality can be added in `tests/locustfile.py`.

### Profiling with py-spy

To profile the app, first get the process id (`pid`) of the running flask app, for example using

```bash
ps | grep flask
```

Then you can record the app's activity using

```bash
py-spy record -o profile.svg --pid <pid>
```

You can interact with the app for a while (or run a `locust` load test), after a while stop the `py-spy` process, which will save a flame graph of the apps activity.

## Deployment

### Deploying on AWS EC2

#### Installing pytorch

We encountered a bug when installing `pytorch` on an AWS EC2 instance, where the installation with `pip` did not finish. To circumvent this, use

```bash
pip install --no-cache-dir torch
```

or, for all requirements,

```bash
pip install -e . --no-cache-dir
```

#### Serving the app

```bash
waitress-serve --call 'chatbot:create_app'
```

#### Ports on AWS EC2

waitress serves the app on port 8080. To redirect to port 80, use

```bash
sudo iptables -t nat -I PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 8080
```

#### Other

Install `git lfs`

```bash
sudo apt install git-lfs
```

### Docker

Docker image is specified in the docker file.

Build the image using

```bash
docker build . --tag chatbot
```

Start the container using

```bash
docker run -p 80:80 --rm chatbot:latest
```

(on mac you have to specify the ports `8080:80 ` because `80` is already in use).

or in interactive mode to inspect the contents:

```bash
docker run -it --rm chatbot:latest bash
```
